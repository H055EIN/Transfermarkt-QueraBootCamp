from typing import List

from sqlalchemy import create_engine, MetaData
from sqlalchemy import URL
from sqlalchemy import text
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, sessionmaker
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


# engine = create_engine(url_object)


def create_database():
    with engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))


def show_database():
    with engine.connect() as conn:
        results = conn.execute(text('SHOW DATABASES;'))
        for res in results:
            return res


engine = create_engine(url_object)


# Base = declarative_base()

class Base(DeclarativeBase):
    pass


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255))
    market_value: Mapped[float] = mapped_column(Float, nullable=True)
    # average_age: Mapped[float] = mapped_column(Float, nullable=True)

    player_stat: Mapped["PlayerStat"] = relationship('PlayerStat', back_populates="team")
    teamstats: Mapped["TeamStat"] = relationship('TeamStat', back_populates="team")
    achievements: Mapped["Achievement"] = relationship('Achievement', back_populates="team")


def __repr__(self):
    return f"Team(id={self.id}, team_name='{self.team_name}', market_value={self.market_value}, average_age={self.average_age})"


class Season(Base):
    __tablename__ = "season"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_at: Mapped[int] = mapped_column(Integer)
    end_at: Mapped[int] = mapped_column(Integer)

    player_stat: Mapped[List["PlayerStat"]] = relationship(back_populates="season")
    teamstats: Mapped[List["TeamStat"]] = relationship(back_populates="season")
    transfers: Mapped[List["Transfer"]] = relationship(back_populates="season")


class Competition(Base):
    __tablename__ = "competition"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competition_name: Mapped[str] = mapped_column(String(128))
    league_id: Mapped[int] = mapped_column(Integer)

    player_stat: Mapped[List["PlayerStat"]] = relationship(back_populates="competition")

    def __repr__(self):
        return f"Season(id={self.id}, name='{self.name}', start_at={self.start_at}, end_at={self.end_at})"


class Achievement(Base):
    __tablename__ = "achievement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cup_name: Mapped[str] = mapped_column(String(128))
    cup_count: Mapped[int] = mapped_column(Integer)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))

    team: Mapped["Team"] = relationship(back_populates="achievements")


class Transfer(Base):
    __tablename__ = "transfer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("season.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    origin_team_id: Mapped[int] = mapped_column(Integer)
    destination_team_id: Mapped[int] = mapped_column(Integer)
    mv: Mapped[float] = mapped_column(Float)
    fee: Mapped[float] = mapped_column(Float)
    joined: Mapped[str] = mapped_column(String(64))
    left: Mapped[str] = mapped_column(String(64))

    player: Mapped["Player"] = relationship(back_populates="transfers")
    season: Mapped["Season"] = relationship(back_populates="transfers")


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    current_team: Mapped[str] = mapped_column(String(128))
    full_name: Mapped[str] = mapped_column(String(128))
    age: Mapped[int] = mapped_column(Integer)
    birth_place: Mapped[str] = mapped_column(String(128))
    height: Mapped[float] = mapped_column(Float)
    citizenship: Mapped[List[str]] = mapped_column(String(128))
    nationality: Mapped[str] = mapped_column(String(64))
    main_position: Mapped[str] = mapped_column(String(64))
    other_position: Mapped[List[str]] = mapped_column(String(128))
    foot: Mapped[str] = mapped_column(String(32))
    total_goals_in_clubs: Mapped[int] = mapped_column(Integer)
    total_assists: Mapped[int] = mapped_column(Integer)
    international_goals: Mapped[int] = mapped_column(Integer)
    caps: Mapped[int] = mapped_column(Integer)
    total_squad: Mapped[int] = mapped_column(Integer)
    total_appearance: Mapped[int] = mapped_column(Integer)
    total_own_goal: Mapped[int] = mapped_column(Integer)
    total_sub_off: Mapped[int] = mapped_column(Integer)
    total_sub_on: Mapped[int] = mapped_column(Integer)
    total_yellow_card: Mapped[int] = mapped_column(Integer)
    total_second_yellow_card: Mapped[int] = mapped_column(Integer)
    total_red_card: Mapped[int] = mapped_column(Integer)
    total_penalty: Mapped[int] = mapped_column(Integer)
    total_minutes_per_goal: Mapped[float] = mapped_column(Float)
    total_minutes_play: Mapped[float] = mapped_column(Float)
    total_goal_conceded: Mapped[int] = mapped_column(Integer)
    total_clean_sheet: Mapped[int] = mapped_column(Integer)
    total_PPG: Mapped[float] = mapped_column(Float)
    highest_market_value: Mapped[float] = mapped_column(Float)
    current_market_value: Mapped[float] = mapped_column(Float)

    player_stat: Mapped[List["PlayerStat"]] = relationship('PlayerStat', back_populates="player")
    transfers: Mapped[List["Transfer"]] = relationship(back_populates="player")


class PlayerStat(Base):
    __tablename__ = "player_stat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    competition_id: Mapped[int] = mapped_column(ForeignKey("competition.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    squad: Mapped[int] = mapped_column(Integer)
    appearance: Mapped[int] = mapped_column(Integer)
    PPG: Mapped[float] = mapped_column(Float)
    goals: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    season_id: Mapped[int] = mapped_column(ForeignKey("season.id"))
    own_goal: Mapped[int] = mapped_column(Integer)
    sub_off: Mapped[int] = mapped_column(Integer)
    sub_on: Mapped[int] = mapped_column(Integer)
    yellow_card: Mapped[int] = mapped_column(Integer)
    second_yellow_card: Mapped[int] = mapped_column(Integer)
    red_card: Mapped[int] = mapped_column(Integer)
    penalty_goals: Mapped[int] = mapped_column(Integer)
    clean_sheets: Mapped[int] = mapped_column(Integer)
    goal_conceded: Mapped[int] = mapped_column(Integer)
    minutes_per_goal: Mapped[int] = mapped_column(Integer)
    minutes_play: Mapped[int] = mapped_column(Integer)

    team: Mapped["Team"] = relationship(back_populates="player_stat")
    player: Mapped["Player"] = relationship(back_populates="player_stat")
    competition: Mapped["Competition"] = relationship(back_populates="player_stat")
    season: Mapped["Season"] = relationship(back_populates="player_stat")


class TeamStat(Base):
    __tablename__ = "teamstat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    season_id: Mapped[int] = mapped_column(ForeignKey("season.id"))
    matches: Mapped[int] = mapped_column(Integer)
    wins: Mapped[int] = mapped_column(Integer)
    losts: Mapped[int] = mapped_column(Integer)
    draws: Mapped[int] = mapped_column(Integer)
    goals: Mapped[int] = mapped_column(Integer)
    goal_differenece: Mapped[int] = mapped_column(Integer)
    pts: Mapped[int] = mapped_column(Integer)

    team: Mapped["Team"] = relationship(back_populates="teamstats")
    season: Mapped["Season"] = relationship(back_populates="teamstats")


Base.metadata.create_all(engine)
