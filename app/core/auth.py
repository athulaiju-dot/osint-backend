import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

API_TOKEN = os.getenv("API_TOKEN")

security = HTTPBearer(auto_error=True)

def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")

    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

    return credentials.credentials
