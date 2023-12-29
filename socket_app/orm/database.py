from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


engine = create_engine("sqlite:///db.sqlite3")

session = sessionmaker(
    engine,
    expire_on_commit=False,
    echo=True,
)

Base = declarative_base()
