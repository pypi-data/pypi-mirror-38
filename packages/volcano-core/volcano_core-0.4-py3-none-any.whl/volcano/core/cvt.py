from volcano.general.stddef import ValueType
from volcano.general.variant import Variant


class StdValueCvt:      # pylint: disable=too-few-public-methods
    def try_convert(self, src_val: Variant, dest_val: Variant) -> bool:     # pylint: disable=no-self-use
        assert isinstance(src_val, Variant), src_val
        assert isinstance(dest_val, Variant), dest_val

        if src_val.is_void() or dest_val.is_void():
            return False

        if src_val.same_type(dest_val):
            dest_val.copy_from_same_type(src_val)
            return True

        if src_val.vt() == ValueType.VT_STR or dest_val.vt() == ValueType.VT_STR:
            return False

        src_t = src_val.vt()
        dest_t = dest_val.vt()
        src_v = src_val.get_value()
        dest_v = None

        if src_v is not None:
            if src_t == ValueType.VT_BOOL:

                # if dest_t == ValueType.VT_BOOL:
                if dest_t == ValueType.VT_INT:
                    dest_v = 1 if src_v else 0
                elif dest_t == ValueType.VT_FLOAT:
                    dest_v = 1.0 if src_v else 0.0
                else:
                    assert False, dest_t

            elif src_t == ValueType.VT_INT:

                if dest_t == ValueType.VT_BOOL:
                    dest_v = True if src_v else False
                # elif dest_t == ValueType.VT_INT:
                elif dest_t == ValueType.VT_FLOAT:
                    dest_v = float(src_v)
                else:
                    assert False, dest_t

            elif src_t == ValueType.VT_FLOAT:

                if dest_t == ValueType.VT_BOOL:
                    dest_v = True if src_v else False
                elif dest_t == ValueType.VT_INT:
                    dest_v = int(src_v)
                # elif dest_t == ValueType.VT_FLOAT:
                else:
                    assert False, dest_t

            else:
                assert False, src_t

        dest_val.set_value_w(dest_v)
        return True
