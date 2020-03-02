from typing import (
    Union,
    Optional,
)

from fastapi import HTTPException
from fastapi.openapi.models import HTTPBearer
from fastapi.security.base import SecurityBase
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from fastapi_security_typeform.custom_types import HashMethodType
from fastapi_security_typeform.hash_methods import hmac_sha256


class SignatureHeader(SecurityBase):
    """
    FastAPI security definition for Typeform HMAC SHA256 signature.
    """

    scheme_name = "signature_header"

    def __init__(
        self,
        *,
        secret: Union[bytes, bytearray],
        signature_prefix: str = "sha256=",
        header_name: str = "Typeform-Signature",
        hash_method: HashMethodType = hmac_sha256,
        auto_error: bool = True
    ):
        self.model = HTTPBearer(scheme=self.scheme_name)
        self.signature_prefix = signature_prefix
        self.secret = secret
        self.header_name = header_name
        self.hash_method = hash_method
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Extract signature from headers and validate it.

        :raises HTTPException: raise 403 error if signature is empty or signature check is failed
        """
        signature: str = request.headers.get(self.header_name)
        if not signature:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None

        payload = await request.body()
        payload_hash = self.hash_method(payload, self.secret,)
        check_signature = self.signature_prefix + payload_hash

        if signature != check_signature:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Bad signature"
                )
            else:
                return None

        return signature
