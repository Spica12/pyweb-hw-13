class Config:
    DB_URL = "postgresql+asyncpg://postgres:567234@localhost:5432/contacts_with_users"
    SECRET_KEY = "c69d646daf018cf7cdd0c8e4a1b6b6b9522327e685ff022f7fbce79517b26dc1"
    ALGORITHM = "HS256"


config = Config()
