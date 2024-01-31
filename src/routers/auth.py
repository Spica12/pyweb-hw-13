from fastapi import (APIRouter, Depends, HTTPException, Path, Query, Security,
                     status)
from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer,
                              OAuth2PasswordRequestForm)
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_db
from src.schemas.user import TokenSchema, UserCreateSchema, UserReadSchema
from src.services.auth import auth_service

router = APIRouter(tags=["auth"])
get_refresh_token = HTTPBearer()


@router.post(
    "/signup", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED
)
async def signup(body: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    exist_user = await auth_service.get_user_by_username(body.username, db=db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await auth_service.create_user(body, db)

    return new_user


@router.post("/login", response_model=TokenSchema)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    # user = await repositories_users.get_user_by_username(body.username, db)
    user = await auth_service.get_user_by_username(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = await auth_service.create_access_token(data={"sub": user.username})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.username})

    await auth_service.update_refresh_token(user, refresh_token, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token", response_model=TokenSchema)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(get_refresh_token),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    username = await auth_service.decode_refresh_token(token)
    user = await auth_service.get_user_by_username(username, db)
    refresh_token = await auth_service.get_refresh_token_by_user(user, db)
    if refresh_token != token:
        await auth_service.update_refresh_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"sub": user.username})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.username})

    await auth_service.update_refresh_token(user, refresh_token, db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
