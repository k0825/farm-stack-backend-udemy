import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config
from typing import Union

JWT_CONFIG = config("JWT_KEY")


class AuthJwtCsrf:
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret_key = JWT_CONFIG

    def generate_hashed_pw(self, password: Union[str, bytes]) -> str:
        return self.pwd_ctx.hash(password)

    def verify_pw(
        self, plain_pw: Union[str, bytes], hash_pw: Union[str, bytes]
    ) -> bool:
        return self.pwd_ctx.verify(plain_pw, hash_pw)

    def encode_jwt(self, email: str) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=5),
            "iat": datetime.utcnow(),
            "sub": email,
        }
        return jwt.encode(
            payload=payload, key=self.secret_key, algorithm="HS256"
        )

    def decode_jwt(self, token) -> str:
        try:
            payload = jwt.decode(
                jwt=token, key=self.secret_key, algorithms=["HS256"]
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="The JWT has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="JWT is not valid")