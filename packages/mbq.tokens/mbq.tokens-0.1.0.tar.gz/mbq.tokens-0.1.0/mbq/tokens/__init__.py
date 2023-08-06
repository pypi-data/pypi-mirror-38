from .decoder import Decoder
from .exceptions import TokenError  # noqa
from .__version__ import (  # noqa
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)


def init(certificate=None, allowed_audiences=None):
    decoder = Decoder(
        certificate=certificate,
        allowed_audiences=allowed_audiences,
    )

    global decode, decode_header, decode_with_unknown_audience
    decode = decoder.decode
    decode_header = decoder.decode_header
    decode_with_unknown_audience = decoder.decode_with_unknown_audience
