import re

from volcano.general.stddef import ValueType

RE_BIT = re.compile(r'(.+) bit (\d+)')


class Expr:

    @staticmethod
    def load_w(expr_str: str, target_tag, db):  # pylint: disable=invalid-name
        assert isinstance(expr_str, str), expr_str

        m = RE_BIT.fullmatch(expr_str)
        if m:
            return ExprBit(expr_str, target_tag, db, m)
        raise Warning('Expression "{}" is invalid. Possible options: "XXX bit N"'.format(expr_str))

    # list of tags
    def sources(self) -> tuple:
        raise NotImplementedError()

    # rval: (value, quality)
    def exec_safe(self, log) -> tuple:
        raise NotImplementedError()


class ExprBit(Expr):
    def __init__(self, expr_str: str, target_tag, db, m):   # pylint: disable=invalid-name, unused-argument
        vt = target_tag.var().vt()
        if vt != ValueType.VT_BOOL:
            raise Warning('Target tag should be BOOL for bit expression. Tag {} is {}'.format(target_tag.full_name(), vt))

        source_name = m.group(1)
        bit_idx_str = m.group(2)

        source = db.resolve_path_w(target_tag, source_name)
        if source.var().vt() != ValueType.VT_INT:
            raise Warning('Source tag should be INT for bit expression. Tag {} is {}'.format(source.full_name(), source.var().vt()))

        try:
            bit_idx = int(bit_idx_str)
        except ValueError as e:
            raise Warning('{} is not a valid bit index: {}'.format(m.group(1), e))

        if bit_idx < 0 or bit_idx > 63:
            raise Warning('{} is not a valid bit index'.format(bit_idx))

        self.bit_mask_ = 1 << bit_idx
        self.src_tag_ = source

    def sources(self) -> tuple:
        return (self.src_tag_,)

    def exec_safe(self, log) -> tuple:
        src_v = self.src_tag_.var().get_value()
        src_q = self.src_tag_.quality

        if src_v is None:
            return None, src_q

        assert isinstance(src_v, int), src_v
        return bool(src_v & self.bit_mask_), src_q
