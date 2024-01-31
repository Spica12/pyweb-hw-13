from fastapi import FastAPI

from src.routers.auth import router as auth
from src.routers.contacts_items import router as contacts_router

app = FastAPI()
app.include_router(contacts_router, prefix="/contacts")
app.include_router(auth, prefix="/auth")


@app.get("/healthchecker")
async def healthchecker():
    return {"message": "Hello World!"}
