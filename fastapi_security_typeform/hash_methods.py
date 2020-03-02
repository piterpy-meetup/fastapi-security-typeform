import hashlib
import hmac
from base64 import b64encode
from typing import Union


def hmac_sha256(payload: bytes, secret: Union[bytes, bytearray]) -> str:
    hashed = hmac.new(key=secret, msg=payload, digestmod=hashlib.sha256).digest()
    base64_encoded = b64encode(hashed)
    return base64_encoded.decode()
