from fastapi import FastAPI
from app.api import image, phone, ip, username

app = FastAPI(title="Advanced OSINT Backend")

app.include_router(image.router, prefix="/osint/image")
app.include_router(phone.router, prefix="/osint/phone")
app.include_router(ip.router, prefix="/osint/ip")
app.include_router(username.router, prefix="/osint/username")

@app.get("/health")
def health():
    return {"status": "online"}
