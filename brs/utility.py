from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from constants import API_TEST_USERNAME, API_TEST_PASSWORD

security = HTTPBasic()


# Basic auth function
def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if (credentials.username != API_TEST_USERNAME or
            credentials.password != API_TEST_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
