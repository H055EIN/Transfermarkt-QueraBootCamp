import json
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from model import Team,Competition

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
session = Session()

with open('..\\web_scraping\\teams.json', 'r') as f:
    data = json.load(f)

for entry in data:
    team_id = entry["id"]
    query = select(Team).filter_by(id=team_id)
    existing_team = session.scalars(query).first()

    if existing_team is None:
        average_age = entry["average_age"].strip()
        market_value = entry["market_value"]
        if isinstance(market_value, str):
            market_value = market_value.replace('€', '').replace('m', '')
        else:
            market_value = None

        team = Team(
            id=team_id,
            team_name=entry["team_name"],
            market_value=market_value,
            average_age=average_age
        )

        

        # Add the team to the session
        session.add(team)

# Commit the changes to the database
session.commit()
