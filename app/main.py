from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ 1. Create the app FIRST
app = FastAPI(title="Advanced OSINT Backend")

# ✅ 2. Add CORS middleware AFTER app is created
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 3. Import routers AFTER app + middleware
from app.api import image, phone, ip, username

# ✅ 4. Include routers
app.include_router(image.router, prefix="/osint/image")
app.include_router(phone.router, prefix="/osint/phone")
app.include_router(ip.router, prefix="/osint/ip")
app.include_router(username.router, prefix="/osint/username")

# ✅ 5. Health check
@app.get("/health")
def health():
    return {"status": "online"}
