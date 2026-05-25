from fastapi import FastAPI
from database import Base, engine
from routers.search import router as search_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

print("BASE_DIR:", BASE_DIR)
print("STATIC_DIR:", STATIC_DIR)
print("STATIC EXISTS:", STATIC_DIR.exists())
print("IMAGES:", list((STATIC_DIR / "images").glob("*")))

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(search_router)


@app.get("/")
def root():
    return {"message": "Clothes search API is running"}