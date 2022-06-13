from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from validator import UserSchema
from typing import Dict
import secrets
import jwt
import time
import env

JWT_SEC = env.TOKEN_SECRET

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jw_token: str) -> bool:
        is_valid: bool = False
        try:
            jwt_init = JWTInit()
            payload = jwt_init.jwt_decode(jw_token)
        except:
            payload = None
        if payload:
            is_valid = True
        return is_valid


class JWTInit:
    def __init__(self):
        self.JWT_SECRET = JWT_SEC
        self.JWT_ALGORITHM = "HS256"

    def jwt_sign(self, user_id: str) -> Dict[str, str]:
        payload = {
            "user_id": user_id,
            "expires": time.time() + 600
        }
        token = jwt.encode(payload, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        return token

    def jwt_decode(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else None
        except:
            return {}


class UserManager:
    def __init__(self):
        self.users = []
        default_credentials_file = open("auth.txt", "r")
        lines = default_credentials_file.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
        default_credentials_file.close()
        self.users.append(UserSchema(**{"username": username, "password": password}))
        self.jwt = JWTInit()

    def check_user(self, data: UserSchema):
        for user in self.users:
            if user.username == data.username and user.password == data.password:
                return {"is_ok": True, "token": self.jwt.jwt_sign(user.username)}
        # Status Code
        return {"is_ok": False}

    def add_user(self, user: UserSchema):
        for registered_user in self.users:
            if user.username == registered_user.username:
                # Status Code
                return {"is_ok": False}
        self.users.append(user)
        # Status Code
        return {"is_ok": True}
