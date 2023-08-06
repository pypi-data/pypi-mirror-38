#!/usr/bin/python3
import enum


class ServerErrorCode(enum.Enum):
    BadVersion = 'bad_version'
    NoHandshake = 'no_handshake'
    NoSlot = 'no_slot'
    SyntaxError = 'bad_syntax'
    ProtocolError = 'protocol_error'


class ServerError(UserWarning):
    def __init__(self, msg: str, code: ServerErrorCode):
        assert isinstance(msg, str), msg
        assert isinstance(code, ServerErrorCode), code

        super().__init__(msg)
        self.code = code


class ServerWarning(UserWarning):
    def __init__(self, msg: str, code: str):
        assert isinstance(msg, str), msg
        assert isinstance(code, str), code

        super().__init__(msg)
        self.code = code
