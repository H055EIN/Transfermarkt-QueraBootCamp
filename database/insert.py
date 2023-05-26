import json
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from model import Team

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

with open('..\\web_scraping\\teams.json') as f:
    data = json.load(f)
unique_team_ids = set()
for entry in data:
    team_id = entry["id"]
    if team_id in unique_team_ids:
        continue
    unique_team_ids.add(team_id)
    # try:
    #     average_age = float(entry["average_age"].strip())
    # except ValueError:
    #     print(repr(entry["average_age"]))
    #     print(team_id)
    #     exit(1)
    market_value = entry["market_value"]

    if isinstance(market_value, str):
        if market_value.endswith('m'):
            market_value = float(market_value[1:-1].strip())
        else:
            market_value = float(market_value[1:-2].strip())
    else:
        market_value = None

    steam = Team(
        id=team_id,
        team_name=entry["team_name"],
        market_value=market_value,
        # average_age=average_age
    )

    # Add the team to the session
    session.add(steam)

# Commit the changes to the database
session.commit()
