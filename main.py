from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


import redis.asyncio as redis

from src.conf.config import config
from src.routers.auth import router as auth
from src.routers.contacts_items import router as contacts_router
from src.routers.users import router as users_router

app = FastAPI()
app.include_router(auth, prefix="/api")
app.include_router(contacts_router, prefix="/api")
app.include_router(users_router, prefix="/api")

app.mount("/static", StaticFiles(directory=config.BASE_DIR / "static"), name="static")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


@app.get("/healthchecker")
async def healthchecker():
    return {"message": "Hello World!"}
