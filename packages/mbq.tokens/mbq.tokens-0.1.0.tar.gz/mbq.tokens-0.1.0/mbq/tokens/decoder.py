import datetime as dt

import jwt
import six
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate

from . import exceptions


class Token:
    """
    Convenience class for easy access to the fields of a JWT.

    All properties use the full name of the claims specified by the
    JWT RFC[1] except for `expires_at` which was changed from
    `expiration_time` to avoid implying that the return value is
    anything other than a datetime.

    The `dict` read-only interface (`__getitem__` and `get`) are
    provided for backwards-compatibility only; new code should use
    the properties.

    [1]: https://tools.ietf.org/html/rfc7519#section-4.1
    """
    def __init__(self, raw, decoded):
        self.raw = raw
        self._decoded = decoded

    def __getitem__(self, key):
        return self._decoded[key]

    def get(self, key, default=None):
        return self._decoded.get(key, default)

    @property
    def issuer(self):
        return self._decoded.get('iss')

    @property
    def subject(self):
        return self._decoded.get('sub')

    @property
    def audience(self):
        return self._decoded.get('aud')

    @property
    def expires_at(self):
        ts = self._decoded.get('exp')
        if ts is None:
            return
        return dt.datetime.fromtimestamp(ts, dt.timezone.utc)

    @property
    def not_before(self):
        ts = self._decoded.get('nbf')
        if ts is None:
            return
        return dt.datetime.fromtimestamp(ts, dt.timezone.utc)

    @property
    def issued_at(self):
        ts = self._decoded.get('iat')
        if ts is None:
            return
        return dt.datetime.fromtimestamp(ts, dt.timezone.utc)


class Decoder:
    def __init__(self, certificate=None, allowed_audiences=None):
        if not certificate:
            m = ('`certificate` must be a string with proper key guards '
                 '(i.e., -----BEGIN CERTIFICATE-----)')
            raise exceptions.TokenError(m)

        err_msg = '`allowed_audiences` must be a list, tuple, or set of strings'
        if not isinstance(allowed_audiences, (list, tuple, set)):
            raise exceptions.TokenError(err_msg)

        if any(not isinstance(aud, six.string_types) for aud in allowed_audiences):
            raise exceptions.TokenError(err_msg)

        try:
            self._public_key = load_pem_x509_certificate(
                certificate.encode(),
                default_backend(),
            ).public_key()
        except Exception as e:
            msg = '`certificate` could not be loaded as a public key. {}'.format(e)
            raise exceptions.TokenError(msg)

        self._allowed_audiences = set(allowed_audiences)

    def _decode(self, token, verify_audience=True):
        try:
            decoded_token = jwt.decode(
                token,
                key=self._public_key,
                options={'verify_aud': False},
                algorithms=['RS256'],
            )
        except Exception as e:
            msg = '`token` could not be decoded. {}'.format(e)
            raise exceptions.TokenError(msg)

        if verify_audience and decoded_token['aud'] not in self._allowed_audiences:
            raise exceptions.TokenError('`aud` claim is not in allowed_audiences')

        return Token(token, decoded_token)

    def decode(self, token):
        return self._decode(token)

    def decode_with_unknown_audience(self, token):
        return self._decode(token, verify_audience=False)

    def decode_header(self, header):
        err_msg = '`header` must be a string in the form "Bearer <token>"'

        if not isinstance(header, six.string_types):
            raise exceptions.TokenError(err_msg)

        try:
            bearer, token = header.strip().split()
        except ValueError:
            raise exceptions.TokenError(err_msg)

        if bearer.lower() != 'bearer':
            raise exceptions.TokenError(err_msg)

        return self.decode(token)
