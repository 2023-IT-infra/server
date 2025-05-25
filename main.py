from fastapi import FastAPI

from router import api_router, auth_router, v0_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 특정 origin만 허용하려면 명시적으로 설정. 예: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # 또는 특정 메서드 ["GET", "POST", "OPTIONS"]
    allow_headers=["*"],
)


app.include_router(api_router)
app.include_router(auth_router)

app.include_router(v0_router)
