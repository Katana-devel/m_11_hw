import contextlib

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.conf.config import config


class DatabaseSessionManager:
    def __init__(self, url: str):
        self.engine: AsyncEngine | None = create_async_engine(url)
        self.session_maker: async_sessionmaker = async_sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextlib.asynccontextmanager
    async def session(self):
        if self.session_maker is None:
            raise Exception("Session is not initialized")
        session = self.session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
