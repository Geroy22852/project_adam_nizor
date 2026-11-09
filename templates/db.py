from sqlalchemy import create_engine, text, Table, Column, Integer, String, MetaData, ForeignKey, insert
from sqlalchemy.orm import sessionmaker, session, DeclarativeBase, Mapped, mapped_column


engine = create_engine("postgresql+psycopg2://postgres:sql@localhost:5432/sport_store", echo=True)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

class ItemsORM(Base):

    __tablename__ = "items"

    id : Mapped[int] = mapped_column(primary_key = True)
    creator : Mapped[str]
    model : Mapped[str]
    price : Mapped[int]

class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str]
    password : Mapped[str]


Base.metadata.create_all(engine) #запустил движок
