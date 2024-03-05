from secrets import compare_digest

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import settings

security = HTTPBasic()


def authenticate(cred: HTTPBasicCredentials = Depends(security)):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    if not cred.username or not cred.password:
        raise error

    if not compare_digest(
        cred.username.encode("utf-8"), settings.EXPENSES_USERNAME.encode("utf-8")
    ):
        raise error
    if not compare_digest(
        cred.password.encode("utf-8"), settings.EXPENSES_PASSWORD.encode("utf-8")
    ):
        raise error
    return True
