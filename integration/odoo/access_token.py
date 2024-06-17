
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel, ValidationError
from jose import JWTError, jwt
from passlib.context import CryptContext

# openssl rand -hex 32
SECRET_KEY = "148c5833fce2bc7789f0600c3bfe8f3294e28bf0df7e3a6d435394701b003921"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*5
ACCESS_TOKEN_EXPIRE_SECONDS = 60*60*10


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
            "me": "Read information about the current user.",
            "items": "Read items.",
            "sales": "Can see sales and products.",
    },
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta: #TODO use now(datetime.UTC)
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validate_token(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"

        credentials_expired = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user: str = payload.get("sub")
            user_type: str = payload.get("user_type")
            code: str = payload.get("code")

            if user is None:
                raise credentials_expired

        except (JWTError, ValidationError) as ex:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(ex),
                headers={"WWW-Authenticate": authenticate_value},
            )

        return {
            'user': user,
            "user_type": user_type,
            "code": code,
            'dateupdate': datetime.now().isoformat()
        }
