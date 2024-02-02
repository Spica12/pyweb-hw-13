from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis


from src.conf.config import config
from src.routers.auth import router as auth
from src.routers.contacts_items import router as contacts_router

app = FastAPI()
app.include_router(contacts_router, prefix="/contacts")
app.include_router(auth, prefix="/auth")


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
