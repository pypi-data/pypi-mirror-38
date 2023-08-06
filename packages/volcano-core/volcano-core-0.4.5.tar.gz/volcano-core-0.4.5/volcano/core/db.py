import subprocess
import shlex
import os.path

from volcano.general import variant
from volcano.general.stddef import Quality, ValueType
from volcano.general import tstamp
from volcano.general.xml_reader import LoadException, load_xml_file_le, XmlReader, get_node_location

from .expr import Expr


class Tag:  # pylint: disable=too-many-instance-attributes
    def __init__(self, parent_n: ('Tag', None), short_name: str, tag_id: int, var: variant.Variant = None, q: Quality = Quality.QUALITY_NOT_INIT):
        assert parent_n is None or isinstance(parent_n, Tag), parent_n
        assert isinstance(short_name, str), short_name
        assert isinstance(tag_id, int), tag_id
        assert var is None or isinstance(var, variant.Variant), var
        assert isinstance(q, Quality), q

        self.parent_ = parent_n  # None
        self.id = tag_id  # pylint: disable=invalid-name
        self.short_name_ = short_name
        self.full_name_ = (parent_n.full_name() + '.' + short_name) if parent_n else short_name
        self.children_ = []
        self.attributes = {}

        self.expr = None
        self.expr_deps = []  # for which tags this one is a part of expression

        self.var_ = var or variant.VOID_VALUE
        if not self.var_.is_void():
            self.quality = q
            self.tstamp_utc = tstamp.get_current_tstamp_utc()

    def vqt_dict_nonvoid(self, include_tstamp: bool = True):
        assert not self.is_void(), self
        assert isinstance(include_tstamp, bool), include_tstamp

        if include_tstamp:
            return {'v': self.var_.get_value(), 'q': self.quality, 't': tstamp.serialize_tstamp(self.tstamp_utc)}
        return {'v': self.var_.get_value(), 'q': self.quality}

    def var(self):
        return self.var_

    def is_void(self):
        return self.var_.is_void()

    def has_children(self):
        return len(self.children_) > 0

    def parent(self):
        return self.parent_

    def short_name(self):
        return self.short_name_

    def enum_child_tags(self):
        return self.children_

    def full_name(self):
        return self.full_name_

    def find_child(self, short_name):
        for x in self.children_:
            if x.short_name() == short_name:
                return x
        return None

    def set_strict(self, value, quality: Quality, ts: 'datetime.datetime') -> None:
        self.var_.set_value_w(value)
        self.quality = quality
        self.tstamp_utc = ts or tstamp.get_current_tstamp_utc()

class Db:
    def __init__(self, log):
        self.root_tags_ = []
        self.all_tags_map_ = {}
        self.all_tags_list_ = []
        self.log = log

    def nb_tags(self) -> int:
        return len(self.all_tags_list_)

    def find_tag_by_name(self, full_name: str) -> (Tag, None):
        assert isinstance(full_name, str), str

        return self.all_tags_map_.get(full_name, None)

    def find_tag_by_id(self, tag_id: int) -> (Tag, None):
        assert isinstance(tag_id, int), tag_id

        if 0 < tag_id <= len(self.all_tags_list_):
            return self.all_tags_list_[tag_id - 1]
        return None

    def find_tag_by_name_or_id(self, tag_name_or_id: (int, str)) -> (Tag, None):
        assert isinstance(tag_name_or_id, (int, str)), tag_name_or_id

        if isinstance(tag_name_or_id, int):
            return self.find_tag_by_id(tag_name_or_id)
        return self.find_tag_by_name(tag_name_or_id)

    def enum_root_tags(self):
        return self.root_tags_

    def all_tags_list(self):
        return self.all_tags_list_

    def create_tag(self, parent_tag_n: (Tag, None), short_name: str, var: variant.Variant = None, q: Quality = Quality.QUALITY_NOT_INIT) -> Tag:
        assert parent_tag_n is None or isinstance(parent_tag_n, Tag), parent_tag_n
        assert isinstance(short_name, str), short_name
        assert var is None or isinstance(var, variant.Variant), var
        assert isinstance(q, Quality), q

        tag_id = len(self.all_tags_list_) + 1
        tag = Tag(parent_tag_n, short_name, tag_id, var, q)
        if parent_tag_n:
            parent_tag_n.children_.append(tag)
        else:
            self.root_tags_.append(tag)

        self.all_tags_list_.append(tag)
        self.all_tags_map_[tag.full_name()] = tag

        return tag

    def create_tag_by_long_name(self, parent_tag_n: (Tag, None), long_name: str, var: variant.Variant = None, q: Quality = Quality.QUALITY_NOT_INIT) -> Tag:
        assert isinstance(long_name, str), long_name
        assert isinstance(q, Quality), q

        if '.' in long_name:  # short name
            names = long_name.split('.')
            parent_name = '.'.join(names[:-1])
            self_name = names[-1]
            my_parent_tag = self.ensure_branch(parent_tag_n, parent_name)
            return self.create_tag(my_parent_tag, self_name, var, q)
        else:
            return self.create_tag(parent_tag_n, long_name, var, q)

    def ensure_branch(self, root_node_n: Tag, long_name: str) -> Tag:
        assert root_node_n is None or isinstance(root_node_n, Tag), root_node_n
        assert isinstance(long_name, str), long_name

        full_name = (root_node_n.full_name() + '.' + long_name) if root_node_n else long_name
        cr = None
        for n in full_name.split('.'):
            child = cr.find_child(n) if cr else self.find_tag_by_name(n)
            if not child:
                child = self.create_tag(cr, n)
            cr = child
        return cr

    def upload_file(self, file_name: str, parent_tag_n: Tag = None) -> None:
        assert parent_tag_n is None or isinstance(parent_tag_n, Tag), parent_tag_n

        file = load_xml_file_le(file_name)
        for node in file.getroot():
            self.upload_xml_node(node, parent_tag_n)

    def setup_demo_mode(self) -> None:
        demo_db_file_name = os.path.dirname(__file__) + '/demo.xml'
        self.upload_file(demo_db_file_name)

    def upload_xml_node(self, node, parent_tag_n: Tag = None) -> None:  # pylint: disable=too-many-statements
        assert parent_tag_n is None or isinstance(parent_tag_n, Tag), parent_tag_n

        p = XmlReader(node)

        if node.tag == 'Tag':
            vt_str = p.get_str('type', ValueType.VT_VOID)
            try:
                vt = ValueType.parse(vt_str)
            except ValueError:
                raise LoadException('Unknown value type: "{}". Available: {}'.format(vt_str, ValueType.VT_ALL_LIST), node)

            var = variant.Variant.from_vt(vt)
            name = p.get_str('name')
            tag = self.create_tag_by_long_name(parent_tag_n, name, var)

            expr_str = p.get_str('expr', '')
            if expr_str:
                try:
                    expr_inst = Expr.load_w(expr_str, tag, self)
                except Warning as e:
                    raise LoadException('{}'.format(e), node)

                for src in expr_inst.sources():
                    assert isinstance(src, Tag)
                    if src == tag:
                        raise LoadException('Cant use self in expression', node)
                    if src.expr:
                        raise LoadException('Cant use chained expressions', node)
                    src.expr_deps.append(tag)
                tag.expr = expr_inst

            for sub_node in node:
                self.upload_xml_node(sub_node, tag)

        elif node.tag == 'File':
            path = p.get_str('path')
            branch = p.get_str('branch', '')
            target_node = self.ensure_branch(parent_tag_n, branch) if branch else parent_tag_n
            try:
                self.upload_file(path, target_node)
            except LoadException as e:  # file is changed and if exc is raised from inside, we wont get info on original location
                raise LoadException('{}: {}'.format(get_node_location(node), e))

        elif node.tag == 'Proc':
            cmd_line = p.get_str('command')
            self.log.info('Upload tags from process %s ...' % cmd_line)
            args = shlex.split(cmd_line)
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  # stderr > stdout
            ctr = 0
            while True:
                line = p.stdout.readline()
                if not line:
                    break
                s = line.strip().decode('utf-8')
                cmd, name, vt_str = s.split()
                if cmd == 'tag':
                    ctr += 1
                    try:
                        vt = ValueType.parse(vt_str)
                    except ValueError:
                        raise LoadException('Unknown value type: "{}". Available: {}'.format(vt_str, ValueType.VT_ALL_LIST))
                    var = variant.Variant.from_vt(vt)
                    self.create_tag_by_long_name(parent_tag_n, name, var)
                    self.log.debug('Added tag %s [%s]' % (name, vt_str))
                else:
                    self.log.warn('Ignored unknown line from process: %s' % s)

            self.log.info('Upload %d tags from process' % ctr)

        elif node.tag == 'Att':
            if not parent_tag_n:
                raise LoadException('Cant use Attributes on top level', node)

            att_name = p.get_str('n')
            att_value = p.get_str('v', '')

            parent_tag_n.attributes[att_name] = att_value

        else:
            raise LoadException('Unknown node name: "{}"'.format(node.tag), node)

    def resolve_path_w(self, branch_tag_n: Tag, path: str) -> Tag:
        assert branch_tag_n is None or isinstance(branch_tag_n, Tag), branch_tag_n
        assert isinstance(path, str), path

        res = branch_tag_n
        for n in path.split('.'):
            if n == '$up':
                if res:
                    res = res.parent()
                else:
                    raise Warning('Cant resolve path {} from {}: went above root'.format(
                        path, branch_tag_n.full_name() if branch_tag_n else '<root>'))
            else:
                if res:
                    res = res.find_child(n)
                else:
                    res = self.find_tag_by_name(n)

                if not res:
                    raise Warning(
                        'Cant resolve path {} from {}: tag {} does not exist'.format(path,
                                                                                     branch_tag_n.full_name() if branch_tag_n else '<root>',
                                                                                     n))

        if not res:
            raise Warning(
                'Cant resolve path {} from {}: stopped on root'.format(path, branch_tag_n.full_name() if branch_tag_n else '<root>'))

        return res
