from sqlmodel import Session, SQLModel, create_engine

from app.config import settings

args = {
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 10,
    "keepalives_count": 5,
}

engine = create_engine(settings.DATABASE_URL,
                       pool_pre_ping=True, connect_args=args)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
