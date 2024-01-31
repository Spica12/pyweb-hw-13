from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_db
from src.models.users import TokenModel, UserModel
from src.schemas.user import UserCreateSchema


class UserRepo:
    def __init__(self, db):
        self.db: AsyncSession = db

    async def get_user_by_username(self, username: str):
        stmt = select(UserModel).filter_by(username=username)
        user = await self.db.execute(stmt)
        user = user.scalar_one_or_none()

        return user

    async def create_user(self, body: UserCreateSchema):
        new_user = UserModel(**body.model_dump())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def update_token(self, user: UserModel, refresh_token: str | None):
        stmt = select(TokenModel).filter_by(user_id=user.id)
        token = await self.db.execute(stmt)
        token = token.scalar_one_or_none()
        if token:
            token.refresh_token = refresh_token
        else:
            new_token = TokenModel(refresh_token=refresh_token, user_id=user.id)
            self.db.add(new_token)
        await self.db.commit()

    async def get_refresh_token(self, user: UserModel):
        stmt = select(TokenModel).filter_by(user_id=user.id)
        token = await self.db.execute(stmt)
        token = token.scalar_one_or_none()

        return token.refresh_token
