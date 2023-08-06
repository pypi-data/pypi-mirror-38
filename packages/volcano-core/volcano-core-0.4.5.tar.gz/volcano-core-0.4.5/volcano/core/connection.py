#!/usr/bin/python3
import json
import json.decoder
from time import perf_counter

from twisted.internet.protocol import connectionDone
from twisted.protocols.basic import LineReceiver

# volcano
from volcano.general import tstamp
from volcano.general import variant

# locals
from .errors import ServerError, ServerWarning, ServerErrorCode
from .msg_parser import MsgParser

PROTOCOL_VERSION = (0, 2, 0)


class Connection(LineReceiver):
    delimiter = b'\n'

    def __init__(self, server, db, env, parent_log):
        self.server = server
        self.db = db            # pylint: disable=invalid-name
        self.env = env
        self.parent_log = parent_log

        self.inst_name_ = None      # None == not handshaked yet
        self.create_tm_ = perf_counter()
        self.log = self.parent_log.getChild('noname')

        self.sub_all_ = None    # (send_tstamp, use_id, , has_ch_uid, ch_uid)
        self.subs_map_ = None   # key=tag_id; value=(send_tstamp, use_id, , has_ch_uid, ch_uid)

    def connectionLost(self, reason=connectionDone):
        self.log.info('Lost connection')
        self.server.forget(self)

    def rawDataReceived(self, data):    # to prevent warnings on not implemented
        raise NotImplementedError()

    def lineReceived(self, line: bytes) -> None:
        assert isinstance(line, bytes), line

        d = line.strip(b' \t\r\n')
        if not d:
            return

        try:
            line_str = d.decode('utf-8', 'strict')
        except UnicodeDecodeError as ex:
            self.log.error('Error decoding command to utf-8: %s. Command: %s', ex, d)
            self.send({'c': 'drop', 'reason': ServerErrorCode.SyntaxError.value, 'comment': str(ex)})
            self.transport.loseConnection()
            return

        self.log.debug('R< ' + line_str)

        try:
            msg = json.loads(line_str)
        except json.decoder.JSONDecodeError as ex:
            self.log.error('%s. Command: %s. Connection will be dropped', ex, line_str)
            self.send({'c': 'drop', 'reason': ServerErrorCode.SyntaxError.value, 'comment': str(ex)})
            self.transport.loseConnection()
            return

        assert isinstance(msg, dict), msg

        try:
            self.process_cmd(msg)
        except ServerError as ex:
            self.log.error('%s. Command: %s. Connection will be dropped', ex, line_str)
            self.send({'c': 'drop', 'reason': ex.code.value, 'comment': str(ex)})
            self.transport.loseConnection()
        except ServerWarning as ex:
            self.log.warning('%s. Command: %s', ex, line_str)

    def process_cmd(self, msg: dict) -> None:
        dr = MsgParser(msg)
        cmd = dr.get_str('c')

        if cmd == 'hello':
            self.on_handshake(msg)
        else:
            if not self.inst_name_:
                raise ServerError('Command not allowed before handshake: {}'.format(msg), ServerErrorCode.ProtocolError)

            if cmd == 'sub':
                self.on_sub(msg)
            elif cmd == 'set':
                self.on_set(msg)
            elif cmd == 'find':
                self.on_find(msg)
            elif cmd == 'echo':
                self.send(msg)
            elif cmd == 'first':
                self.on_first(msg)
            elif cmd == 'next':
                self.on_next(msg)
            else:
                raise ServerError('Unknown message type "{}" in message {}'.format(cmd, msg), ServerErrorCode.ProtocolError)

    def on_handshake(self, msg: dict) -> None:
        if self.inst_name_:
            raise ServerError('Duplicated handshake message', ServerErrorCode.ProtocolError)

        dr = MsgParser(msg)

        inst_name = dr.get_str('name')
        proto_ver_s = dr.get_str('protocol')

        proto_ver = proto_ver_s.split('.')
        if len(proto_ver) not in (2, 3):
            raise ServerError('Invalid protocol version {}. Should be x.y or x.y.z'.format(proto_ver_s), ServerErrorCode.ProtocolError)

        try:
            clt_major = int(proto_ver[0])
            clt_minor = int(proto_ver[1])
        except ValueError:
            raise ServerError('Invalid protocol version {}. Should be x.y or x.y.z'.format(proto_ver_s), ServerErrorCode.ProtocolError)

        if clt_major != PROTOCOL_VERSION[0] or clt_minor > PROTOCOL_VERSION[1]:
            raise ServerError('Protocol version mismatch. Server: {}.{}.{}, client: {}'.format(PROTOCOL_VERSION[0], PROTOCOL_VERSION[1], PROTOCOL_VERSION[2], proto_ver_s), ServerErrorCode.BadVersion)

        self.inst_name_ = inst_name
        self.log = self.parent_log.getChild(self.inst_name_)
        self.log.debug('Connection renamed to "%s"', self.inst_name_)

        resp = {'c': 'welcome'}
        if 'ch' in msg:     # канал нужен в hs, потому что hs реализуется через сервисы, а они все работают на каналах
            resp['ch'] = msg['ch']

        self.send(resp)

    def on_set(self, msg):
        dr = MsgParser(msg)

        tag_name_or_id = dr.get_tag('tag')
        val_raw = dr.get_raw('v', allow_none=True)
        quality = dr.get_int('q', allow_none=False, optional=True, default=0)
        ts = dr.get_datetime('t', optional=True) or tstamp.get_current_tstamp_utc()

        tag = self.db.find_tag_by_name_or_id(tag_name_or_id)
        if not tag:
            raise ServerWarning('Cant set: tag {} doesnt exist'.format(tag_name_or_id), 'tag_not_found')

        if tag.is_void():
            raise ServerWarning('Cant set: tag {} is VOID'.format(tag.full_name()), 'tag_is_void')

        if tag.expr:
            raise ServerWarning('Cant set: tag {} is calculated'.format(tag.full_name()), 'tag_is_const')

        if val_raw is None:
            if tag.var().get_value() is None and tag.quality == quality:
                return
            tag.var().set_value_w(None)
        else:
            var = variant.Variant.try_from_raw_value(val_raw)
            if var is None:
                raise ServerError('Cant set tag {}={}: unable to detect value type'.format(tag_name_or_id, val_raw), ServerErrorCode.ProtocolError)

            tag_var_copy = tag.var().clone()
            if not self.server.value_cvt().try_convert(var, tag_var_copy):
                raise ServerWarning('Cant set "{}={}": value type mismatch'.format(tag.full_name(), val_raw), 'tag_value_type_mismatch')

            if tag_var_copy == tag.var() and tag.quality == quality:
                return

            tag.var().copy_from_same_type(tag_var_copy)

        tag.quality = quality
        tag.tstamp_utc = ts

        if self.env.log_tag_upd:
            self.log.debug('Set {}={}'.format(tag.full_name(), tag.var()))

        for c in self.server.connections:
            c.notify_update(tag)

        for dep in tag.expr_deps:
            assert dep.expr
            v, q = dep.expr.exec_safe(self.log)
            if not dep.var().val_equal(v, none_eq_none=True) or dep.quality != q:
                dep.var().set_value_w(v)
                dep.quality = q
                for c in self.server.connections:
                    c.notify_update(dep)

    def on_sub(self, msg):
        dr = MsgParser(msg)

        tag_name_or_id = dr.get_tag('tag')
        send_tstamp = dr.get_bool('tstamp', optional=True, default=True)
        ref = dr.get_str('ref', allow_none=True, optional=True, default='')

        has_ch_uid = 'ch' in msg
        ch_uid = msg['ch'] if has_ch_uid else None

        if not ref or ref == 'auto':
            upd_use_id = True if tag_name_or_id == '*' else isinstance(tag_name_or_id, int)
        elif ref == 'id':
            upd_use_id = True
        elif ref == 'name':
            upd_use_id = False
        else:
            raise ServerError('Parameter "ref={}" is invalid. Available: auto|name|id'.format(ref), ServerErrorCode.ProtocolError)

        # Примечание
        # Поскольку у нас отсутствует этап синхронизации, тот, кто подписывается, должен сразу получить актуальное значение.
        # Раньше он моге сделать find(), чтобы понять начальное значение, но теперь это бессмысленно, потому что
        # процессы все уже запущены, и между find/sub значение могло поменяться
        if tag_name_or_id == '*':  # subscribe all
            if self.sub_all_:
                raise ServerError('Duplicated all-subscription', ServerErrorCode.ProtocolError)

            if self.subs_map_:
                raise ServerError('All-subscription not allowed after single', ServerErrorCode.ProtocolError)

            self.sub_all_ = (send_tstamp, upd_use_id, has_ch_uid, ch_uid)

            self.log.debug('%s subscribed all', self.inst_name_)
            # см. Примечание
            for tag in self.db.all_tags_list():
                if not tag.is_void():
                    self.notify_update(tag)
        else:
            if self.sub_all_:
                raise ServerError('Cant subscribe on "{}": all-subscription is already enabled'.format(tag_name_or_id), ServerErrorCode.ProtocolError)

            tag = self.db.find_tag_by_name_or_id(tag_name_or_id)
            if not tag:
                raise ServerWarning('Cant subscribe: tag "{}" doesnt exist'.format(tag_name_or_id), 'tag_not_found')

            if tag.is_void():
                raise ServerWarning('Cant subscribe: tag "{}" is VOID'.format(tag_name_or_id), 'tag_is_void')

            if self.subs_map_ is None:
                self.subs_map_ = {}
            self.subs_map_[tag.id] = (send_tstamp, upd_use_id, has_ch_uid, ch_uid)
            self.log.debug('%s subscribed %s', self.inst_name_, tag.full_name())
            # см. Примечание
            self.notify_update(tag)

    def notify_update(self, tag):
        if self.sub_all_:
            tpl = self.sub_all_
        elif self.subs_map_:
            tpl = self.subs_map_.get(tag.id, None)
        else:
            tpl = None

        if tpl:
            send_tstamp, use_id, has_ch_uid, ch_uid = tpl
            resp = {'c': 'upd', 'tag': tag.id if use_id else tag.full_name(), **tag.vqt_dict_nonvoid(send_tstamp)}
            if has_ch_uid:
                resp['ch'] = ch_uid
            self.send(resp)

    def on_find(self, msg: dict) -> None:
        dr = MsgParser(msg)

        tag_name_or_id = dr.get_tag('tag')

        tag = self.db.find_tag_by_name_or_id(tag_name_or_id)

        if tag:
            res = {'c': 'find_ok', 'id': tag.id, 'name': tag.full_name(), 'type': tag.var().type_str()}
        else:
            res = {'c': 'find_err', 'tag': tag_name_or_id}

        if 'ch' in msg:
            res['ch'] = msg['ch']

        self.send(res)

    def on_first(self, msg: dict) -> None:
        all_lst = self.db.all_tags_list()
        if all_lst:
            tag = all_lst[0]
            resp = {'c': 'next_tag', 'id': tag.id, 'name': tag.full_name(), 'type': tag.var().type_str(), 'atts': tag.attributes}
        else:
            resp = {'c': 'next_end'}

        if 'ch' in msg:
            resp['ch'] = msg['ch']

        self.send(resp)

    def on_next(self, msg: dict) -> None:
        dr = MsgParser(msg)

        tag_name_or_id = dr.get_tag('tag')

        prev = self.db.find_tag_by_name_or_id(tag_name_or_id)

        if prev:
            tag = self.db.find_tag_by_id(prev.id + 1)

            if tag:
                resp = {'c': 'next_tag', 'id': tag.id, 'name': tag.full_name(), 'type': tag.var().type_str(), 'atts': tag.attributes}
            else:
                resp = {'c': 'next_end'}
        else:
            resp = {'c': 'next_err'}

        if 'ch' in msg:
            resp['ch'] = msg['ch']

        self.send(resp)

    def send(self, msg: dict) -> None:
        assert isinstance(msg, dict), msg

        # Ошибки dumps НЕ перехватываем. Они могут быть вызваны только проблемами в коде
        s = json.dumps(msg)     # могут быть разные ошибки. мне попадалась TypeError, но есть еще json.encoder...
        self.log.debug('S> ' + s)
        self.sendLine(s.encode('utf-8'))
