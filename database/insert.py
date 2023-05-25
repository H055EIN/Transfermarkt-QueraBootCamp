import json
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
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

with open('..\\web_scraping\\teams.json', 'r') as f:
    data = json.load(f)

teams = [Team(id=t['id'], team_name=t['team_name'], market_value=t['market_value'], average_age=t['average_age'],)
         for t in data]

session.add_all(teams)
