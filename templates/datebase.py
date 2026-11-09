from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Table, Column, Integer, String, MetaData, ForeignKey, insert
load_dotenv()

metadata = MetaData()

engine = create_engine(
    "postgresql+psycopg2://postgres:admin@localhost:5432/postgres",
    echo=True,
    pool_size=10,
    max_overflow=10
)

with engine.connect() as connect:
    result = connect.execute(text("select * from qwerty"))
    connect.commit()
    print(result.fetchall())

person = Table(
    "person",
    metadata,
    Column[int]("id", Integer, primary_key=True),
    Column[str]("name", String(50)),
    Column[int]("age", Integer),
    Column[str]("gender", String(50)),
)

Card = Table(
        "card",
    metadata,
    Column("id", Integer, primery_key=True),
    Column("name", String(50)),
    Column("price", Integer),
    Column("person_id", Integer, ForeignKey('person.id'))
)

def create_tables():
    metadata.create_all(engine)

create_tables()

