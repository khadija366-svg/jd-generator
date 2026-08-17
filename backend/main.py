from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import jd

app = FastAPI(title="JD Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jd.router)


@app.get("/health")
def health():
    return {"status": "ok"}
