"""File generated by TLObjects' generator. All changes will be ERASED"""
from ...tl.tlobject import TLObject
from ...tl.tlobject import TLRequest
from typing import Optional, List, Union, TYPE_CHECKING
import os
import struct
if TYPE_CHECKING:
    from ...tl.types import TypeDataJSON, TypeInputAppEvent



class AcceptTermsOfServiceRequest(TLRequest):
    CONSTRUCTOR_ID = 0xee72f79a
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, id):
        """
        :param TypeDataJSON id:

        :returns Bool: This type has no constructors.
        """
        self.id = id  # type: TypeDataJSON

    def to_dict(self):
        return {
            '_': 'AcceptTermsOfServiceRequest',
            'id': self.id.to_dict() if isinstance(self.id, TLObject) else self.id
        }

    def __bytes__(self):
        return b''.join((
            b'\x9a\xf7r\xee',
            bytes(self.id),
        ))

    @classmethod
    def from_reader(cls, reader):
        _id = reader.tgread_object()
        return cls(id=_id)


class GetAppChangelogRequest(TLRequest):
    CONSTRUCTOR_ID = 0x9010ef6f
    SUBCLASS_OF_ID = 0x8af52aac

    def __init__(self, prev_app_version):
        """
        :param str prev_app_version:

        :returns Updates: Instance of either UpdatesTooLong, UpdateShortMessage, UpdateShortChatMessage, UpdateShort, UpdatesCombined, Updates, UpdateShortSentMessage.
        """
        self.prev_app_version = prev_app_version  # type: str

    def to_dict(self):
        return {
            '_': 'GetAppChangelogRequest',
            'prev_app_version': self.prev_app_version
        }

    def __bytes__(self):
        return b''.join((
            b'o\xef\x10\x90',
            self.serialize_bytes(self.prev_app_version),
        ))

    @classmethod
    def from_reader(cls, reader):
        _prev_app_version = reader.tgread_string()
        return cls(prev_app_version=_prev_app_version)


class GetAppUpdateRequest(TLRequest):
    CONSTRUCTOR_ID = 0xae2de196
    SUBCLASS_OF_ID = 0x5897069e

    def to_dict(self):
        return {
            '_': 'GetAppUpdateRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'\x96\xe1-\xae',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class GetCdnConfigRequest(TLRequest):
    CONSTRUCTOR_ID = 0x52029342
    SUBCLASS_OF_ID = 0xecda397c

    def to_dict(self):
        return {
            '_': 'GetCdnConfigRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'B\x93\x02R',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class GetConfigRequest(TLRequest):
    CONSTRUCTOR_ID = 0xc4f9186b
    SUBCLASS_OF_ID = 0xd3262a4a

    def to_dict(self):
        return {
            '_': 'GetConfigRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'k\x18\xf9\xc4',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class GetDeepLinkInfoRequest(TLRequest):
    CONSTRUCTOR_ID = 0x3fedc75f
    SUBCLASS_OF_ID = 0x984aac38

    def __init__(self, path):
        """
        :param str path:

        :returns help.DeepLinkInfo: Instance of either DeepLinkInfoEmpty, DeepLinkInfo.
        """
        self.path = path  # type: str

    def to_dict(self):
        return {
            '_': 'GetDeepLinkInfoRequest',
            'path': self.path
        }

    def __bytes__(self):
        return b''.join((
            b'_\xc7\xed?',
            self.serialize_bytes(self.path),
        ))

    @classmethod
    def from_reader(cls, reader):
        _path = reader.tgread_string()
        return cls(path=_path)


class GetInviteTextRequest(TLRequest):
    CONSTRUCTOR_ID = 0x4d392343
    SUBCLASS_OF_ID = 0xcf70aa35

    def to_dict(self):
        return {
            '_': 'GetInviteTextRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'C#9M',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class GetNearestDcRequest(TLRequest):
    CONSTRUCTOR_ID = 0x1fb33026
    SUBCLASS_OF_ID = 0x3877045f

    def to_dict(self):
        return {
            '_': 'GetNearestDcRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'&0\xb3\x1f',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class GetProxyDataRequest(TLRequest):
    CONSTRUCTOR_ID = 0x3d7758e1
    SUBCLASS_OF_ID = 0x21e2a448

    def to_dict(self):
        return {
            '_': 'GetProxyDataRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'\xe1Xw=',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class GetRecentMeUrlsRequest(TLRequest):
    CONSTRUCTOR_ID = 0x3dc0f114
    SUBCLASS_OF_ID = 0xf269c477

    def __init__(self, referer):
        """
        :param str referer:

        :returns help.RecentMeUrls: Instance of RecentMeUrls.
        """
        self.referer = referer  # type: str

    def to_dict(self):
        return {
            '_': 'GetRecentMeUrlsRequest',
            'referer': self.referer
        }

    def __bytes__(self):
        return b''.join((
            b'\x14\xf1\xc0=',
            self.serialize_bytes(self.referer),
        ))

    @classmethod
    def from_reader(cls, reader):
        _referer = reader.tgread_string()
        return cls(referer=_referer)


class GetSupportRequest(TLRequest):
    CONSTRUCTOR_ID = 0x9cdf08cd
    SUBCLASS_OF_ID = 0x7159bceb

    def to_dict(self):
        return {
            '_': 'GetSupportRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'\xcd\x08\xdf\x9c',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class GetTermsOfServiceUpdateRequest(TLRequest):
    CONSTRUCTOR_ID = 0x2ca51fd1
    SUBCLASS_OF_ID = 0x293c2977

    def to_dict(self):
        return {
            '_': 'GetTermsOfServiceUpdateRequest'
        }

    def __bytes__(self):
        return b''.join((
            b'\xd1\x1f\xa5,',
        ))

    @classmethod
    def from_reader(cls, reader):
        return cls()


class SaveAppLogRequest(TLRequest):
    CONSTRUCTOR_ID = 0x6f02f748
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, events):
        """
        :param List[TypeInputAppEvent] events:

        :returns Bool: This type has no constructors.
        """
        self.events = events  # type: List[TypeInputAppEvent]

    def to_dict(self):
        return {
            '_': 'SaveAppLogRequest',
            'events': [] if self.events is None else [x.to_dict() if isinstance(x, TLObject) else x for x in self.events]
        }

    def __bytes__(self):
        return b''.join((
            b'H\xf7\x02o',
            b'\x15\xc4\xb5\x1c',struct.pack('<i', len(self.events)),b''.join(bytes(x) for x in self.events),
        ))

    @classmethod
    def from_reader(cls, reader):
        reader.read_int()
        _events = []
        for _ in range(reader.read_int()):
            _x = reader.tgread_object()
            _events.append(_x)

        return cls(events=_events)


class SetBotUpdatesStatusRequest(TLRequest):
    CONSTRUCTOR_ID = 0xec22cfcd
    SUBCLASS_OF_ID = 0xf5b399ac

    def __init__(self, pending_updates_count, message):
        """
        :param int pending_updates_count:
        :param str message:

        :returns Bool: This type has no constructors.
        """
        self.pending_updates_count = pending_updates_count  # type: int
        self.message = message  # type: str

    def to_dict(self):
        return {
            '_': 'SetBotUpdatesStatusRequest',
            'pending_updates_count': self.pending_updates_count,
            'message': self.message
        }

    def __bytes__(self):
        return b''.join((
            b'\xcd\xcf"\xec',
            struct.pack('<i', self.pending_updates_count),
            self.serialize_bytes(self.message),
        ))

    @classmethod
    def from_reader(cls, reader):
        _pending_updates_count = reader.read_int()
        _message = reader.tgread_string()
        return cls(pending_updates_count=_pending_updates_count, message=_message)

