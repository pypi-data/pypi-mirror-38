from volcano.general import tstamp


from .errors import ServerError, ServerErrorCode


class MsgParser:
    def __init__(self, msg: dict):
        assert isinstance(msg, dict), msg
        self.msg_ = msg

    def get_raw(self, name: str, allow_none: bool = False, optional: bool = False, default=None):
        assert isinstance(name, str), name
        assert isinstance(allow_none, bool), allow_none
        assert isinstance(optional, bool), optional

        if name not in self.msg_:
            if optional:
                return default
            raise ServerError('Parameter {} is missing'.format(name), ServerErrorCode.ProtocolError)

        v = self.msg_[name]
        if v is None:
            if allow_none:
                return None
            raise ServerError('Parameter {} is None'.format(name), ServerErrorCode.ProtocolError)

        return v

    # options should consist of str. None should not be put there
    def get_str(self, name: str, allow_none: bool = False, optional: bool = False, default=None, options: (list, tuple)=None) -> (str, None):
        assert isinstance(name, str), name
        assert isinstance(allow_none, bool), allow_none
        assert isinstance(optional, bool), optional
        assert options is None or isinstance(options, (list, tuple)), options

        if name not in self.msg_:
            if optional:
                return default
            raise ServerError('Parameter {} is missing'.format(name), ServerErrorCode.ProtocolError)

        v = self.msg_[name]
        if v is None:
            if allow_none:
                return None
            raise ServerError('Parameter {} is None'.format(name), ServerErrorCode.ProtocolError)

        if not isinstance(v, str):
            raise ServerError('Parameter {}={} should be str, not {}'.format(name, v, type(v)), ServerErrorCode.ProtocolError)

        if options and v not in options:
            raise ServerError('Parameter {}={} is invalid, available values: {}'.format(name, v, options), ServerErrorCode.ProtocolError)

        return v

    def get_bool(self, name: str, allow_none: bool = False, optional: bool = False, default=None) -> (bool, None):
        assert isinstance(name, str), name
        assert isinstance(allow_none, bool), allow_none
        assert isinstance(optional, bool), optional

        if name not in self.msg_:
            if optional:
                return default
            raise ServerError('Parameter {} is missing'.format(name), ServerErrorCode.ProtocolError)

        v = self.msg_[name]
        if v is None:
            if allow_none:
                return None
            raise ServerError('Parameter {} is None'.format(name), ServerErrorCode.ProtocolError)

        if not isinstance(v, bool):
            raise ServerError('Parameter {}={} should be bool, not {}'.format(name, v, type(v)), ServerErrorCode.ProtocolError)

        return v

    def get_int(self, name: str, allow_none: bool = False, optional: bool = False, default=None) -> (str, None):
        assert isinstance(name, str), name
        assert isinstance(allow_none, bool), allow_none
        assert isinstance(optional, bool), optional

        if name not in self.msg_:
            if optional:
                return default
            raise ServerError('Parameter {} is missing'.format(name), ServerErrorCode.ProtocolError)

        v = self.msg_[name]
        if v is None:
            if allow_none:
                return None
            raise ServerError('Parameter {} is None'.format(name), ServerErrorCode.ProtocolError)

        if not isinstance(v, int):
            raise ServerError('Parameter {}={} should be int, not {}'.format(name, v, type(v)), ServerErrorCode.ProtocolError)

        return v

    def get_datetime(self, name: str, optional: bool = False) -> ('datetime.datetime', None):
        s = self.get_str(name, allow_none=True, optional=optional, default=None)
        try:
            return tstamp.deserialize_tstamp_w(s) if s else None
        except Warning as ex:
            raise ServerError('Parameter {}={} is invalid: {}'.format(name, s, ex), ServerErrorCode.ProtocolError)

    def get_tag(self, name: str, allow_none: bool = False, optional: bool = False, default=None) -> (int, str, None):
        assert isinstance(name, str), name
        assert isinstance(allow_none, bool), allow_none
        assert isinstance(optional, bool), optional

        if name not in self.msg_:
            if optional:
                return default
            raise ServerError('Parameter {} is missing'.format(name), ServerErrorCode.ProtocolError)

        v = self.msg_[name]
        if v is None:
            if allow_none:
                return None
            raise ServerError('Parameter {} is None'.format(name), ServerErrorCode.ProtocolError)

        if not isinstance(v, (int, str)):
            raise ServerError('Parameter {}={} should be (int,str), not {}'.format(name, v, type(v)), ServerErrorCode.ProtocolError)

        return v
