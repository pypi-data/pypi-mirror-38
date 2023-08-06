from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

from volcano.general import tstamp


class TTYControlPanel(LineReceiver):
    delimiter = b'\n'

    def __init__(self, server):
        super().__init__()
        self.server = server
        self.last_cmd_ = None
        self.cwd_ = None

    def rawDataReceived(self, data):    # to prevent warnings on not implemented
        raise NotImplementedError()

    def lineReceived(self, line: bytes):
        s = line.decode('utf-8').strip()
        if s:
            self.last_cmd_ = s
            self.on_cmd(s)
        else:
            if self.last_cmd_:
                print(self.last_cmd_)
                self.on_cmd(self.last_cmd_)
            else:
                pass

    def on_cmd(self, cmd_str):
        items = cmd_str.split(' ')
        if not items:
            return

        try:
            cmd = items[0]
            if cmd == 'cd':
                self.cmd_cd_w(items)
            elif cmd == 'ls':
                self.cmd_ls_w(items)
            elif cmd == 'set':
                self.cmd_set_w(items)
            elif cmd == 'exit':
                reactor.stop()  # pylint: disable=no-member
            else:
                print('Unknown command: {}'.format(cmd))
        except Warning as ex:
            print(ex)

    def cmd_cd_w(self, items):

        def prn_tag(tag):
            if tag.has_children():
                if tag.is_void():
                    print('  > {:10}'.format(tag.short_name()))
                else:
                    print('  > {:10} {} {}'.format(tag.short_name(), tag.var().get_value(), tag.var().type_str()))
            else:
                if tag.is_void():
                    print('  - {:10}'.format(tag.short_name()))
                else:
                    print('  - {:10} {} {}'.format(tag.short_name(), tag.var().get_value(), tag.var().type_str()))

        if len(items) == 1:  # go to root
            self.cwd_ = None
            for child in self.server.db.enum_root_tags():
                prn_tag(child)

        elif len(items) == 2:
            tag_name = items[1]
            tag = self.server.db.find_tag_by_name(
                self.cwd_.full_name() + '.' + tag_name) if self.cwd_ else self.server.db.find_tag_by_name(tag_name)
            if tag:
                self.cwd_ = tag
                for child in tag.enum_child_tags():
                    prn_tag(child)
            else:
                raise Warning('Tag not found: {}'.format(tag_name))
        else:
            raise Warning('Expected 0 or 1 parameter')

    def cmd_ls_w(self, items):
        if len(items) == 1:
            for child in self.server.db.enum_root_tags():
                self.print_tag(child)

        elif len(items) == 2:
            tag_name = items[1]
            tag = self.server.db.find_tag_by_name(tag_name)
            if tag:
                for child in tag.enum_child_tags():
                    self.print_tag(child)
            else:
                raise Warning('Tag not found: {}'.format(tag_name))
        else:
            raise Warning('Expected 0 or 1 parameter')

    def cmd_set_w(self, items):
        if len(items) != 3:
            raise Warning('Expected 2 parameters: set TAG_NAME VALUE')

        tag_name = items[1]
        value_str = items[2]

        tag = self.server.db.find_tag_by_name(tag_name)
        if not tag:
            raise Warning('Tag not found: {}'.format(tag_name))

        if tag.is_void():
            raise Warning('Tag is VOID: {}'.format(tag_name))

        tag.var().parse_value_w(value_str)
        tag.quality = 0
        tag.tstamp_utc = tstamp.get_current_tstamp_utc()

        for c in self.server.connections:
            c.notify_update(tag)

    def print_tag(self, tag): # pylint: disable=no-self-use
        if tag.is_void():
            print('  - {:10}'.format(tag.short_name()))
        else:
            print('  - {:10} {} {}'.format(tag.short_name(), tag.var().get_value(), tag.var().type_str()))
