from sqlalchemy import create_engine, MetaData
from sqlalchemy import URL
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer,Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

DB_NAME = 'Transfermarkt_database'

url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="suramii78",
    host="localhost",
    database=DB_NAME

)

engine = create_engine(url_object)
Session = sessionmaker(bind=engine)


def create_database():
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))


def show_database():
    with engine.connect() as conn:
        results = conn.execute(text('SHOW DATABASES;'))
        for res in results:
            return res


Base = declarative_base()


class Team(Base):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(64))
    market_value: Mapped[float] = mapped_column(Float)
    average_age: Mapped[float] = mapped_column(Float)


def __repr__(self):
    return f"Team(id={self.id}, team_name='{self.team_name}', market_value={self.market_value}, average_age={self.average_age})"


class Season(Base):
    __tablename__ = 'season'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season: Mapped[str] = mapped_column(String(128))
    start_at: Mapped[int] = mapped_column(Integer)
    end_at: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"Season(id={self.id}, name='{self.name}', start_at={self.start_at}, end_at={self.end_at})"


class Competition(Base):
    __tablename__ = 'competition'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competition_name: Mapped[str] = mapped_column(String(128))
    league_id: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"Season(id={self.id}, name='{self.name}', start_at={self.start_at}, end_at={self.end_at})"




Base.metadata.create_all(engine)
