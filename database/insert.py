import json
import os
import numpy as np
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from model import Team,Season,Competition,Achievement,Transfer,PlayerStat,Player

DB_NAME = 'Transfermarkt_database'

url_object = URL.create(
    "mysql+mysqlconnector",
    username="root",
    password="1234",
    host="localhost",
    database=DB_NAME
)

engine = create_engine(url_object)
Session = sessionmaker(bind=engine)
session = Session()

# adding Season
for i in range(15,23):
    sseason = Season(
        start_at = i,
        
    )
    session.add(sseason)


# adding Team and Achievement
os.chdir('./web_scraping')
with open('teams.json' , "r") as f:
    data_team = json.load(f)

extra_team = Team(
    id=0,
    team_name="Others",
    market_value=None,
)
session.add(extra_team)
unique_team_ids = set()
for entry in data_team:
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
    session.add(steam)    

    for cup in entry["cups"] : 
        sachievement = Achievement(
            cup_name = cup[0],
            cup_count = cup[1],
            team_id = steam.id
        )
        session.add(sachievement)


# add Competition
with open('P2_competitions.json') as f2:
    data_competition = json.load(f2)


    for entry2 in data_competition:
        scompetition = Competition(
        competition_name = entry2["Competition"]
        )
        session.add(scompetition)

# add Player
with open('Players.json') as f3:
    data_player = json.load(f3)

def to_minute(string):
    if string:
        if len(string) >4 :
            return int(string.replace("'","").replace(".",""))
        else:
            return int(string.replace("'",""))
    else:
        return None

def correct_value(string):
    if string != "-":
        if string[-1] == "m":
            return float(string.replace("m","")) * 1000000
        else:
            return float(string.replace("k","")) * 1000
    else:
        return None

for player in data_player:
    splayer = Player(
        id = player["id"],
        current_team = player["Current club"],
        full_name = player["full_name"],
        age = int(player["age"]) if player["age"] else None,
        birth_place = player["birth_place"],
        height = float(player["height"].replace(",","").replace(" ","").replace("m","")) if (player["height"]) and (player["height"] != 'N/A') else None,
        citizenship = ",".join(player["citizenship"]),
        nationality = player['nationality'],
        main_position = player["main_position"],
        other_position = ",".join(player['available_positions']),
        foot = player["foot"],
        total_goals_in_clubs = int(player["total_goals_in_clubs"]) if player["total_goals_in_clubs"] != "-" else 0,
        total_assists = int(player["total_assists"]) if (player["total_assists"] != "-") and player["total_assists"] else None,
        international_goals = int(player["international_goals"]) if player["international_goals"] else None,
        caps = int(player["caps"]) if player["caps"] else None,
        total_squad = player["total_squad"],
        total_appearance = int(player["total_apperance"]) if player["total_goals_in_clubs"] != "-" else None,
        total_own_goal = int(player["total_own_goal"]) if player["total_own_goal"] != "-" else 0,
        total_sub_off = int(player["total_sub_off"]) if player["total_sub_off"] != "-" else 0,
        total_sub_on = int(player["total_sub_on"]) if player["total_sub_on"] != "-" else 0,
        total_yellow_card = int(player["total_yellow_card"]) if player["total_yellow_card"] != "-" else 0,
        total_second_yellow_card = int(player["total_second_yellow_card"]) if player["total_second_yellow_card"] != "-" else 0,
        total_red_card = int(player["total_red_card"]) if player["total_red_card"] != "-" else 0,
        total_penalty = int(player["total_penalty"]) if (player["total_penalty"] != "-") and player["total_penalty"] else 0,
        total_minutes_per_goal = to_minute(player["total_minutes_per_goal"]) if player["total_minutes_per_goal"] != "-" else 0,
        total_minutes_play = to_minute(player["total_minutes_per_goal"]) if player["total_minutes_per_goal"] != "-" else 0,
        total_goal_conceded = int(player["total_goal_conceded"]) if (player["total_goal_conceded"]) and (player["total_goal_conceded"] != "-") else None,
        total_clean_sheet = int(player["total_clean_sheets"]) if (player["total_clean_sheets"]) and (player["total_clean_sheets"] != "-") else None,
        total_PPG = float(player["total_ppg"]) if (player["total_ppg"] != "-") and (player["total_ppg"] != '') else None,
        highest_market_value = correct_value(player["highest_market_value"]) if player["highest_market_value"] else None,
        current_market_value = correct_value(player["current_market_value"]) if player["current_market_value"] else None,

    ) 
    session.add(splayer)

# add Player stat

def ppg_fix(string):
    if string == "-":
        return None
    elif len(string)>1 and string[1] == ",":
        return float(string.replace(",","."))
    else:
        return float(string)

with open('P2_player_state.json') as f4:
    data_playerstat = json.load(f4)
for data in data_playerstat:
    q1 = select(Player).filter_by(id=data["Player_id"])
    q_player_id = session.scalars(q1).first()

    
    q_competition_id = session.query(Competition).filter_by(competition_name=data["Competition"]).first()
    
    q_season_id = session.query(Season).filter_by(start_at=int(data["Season"][0:2])).first()
    q_team_id = session.query(Team).filter_by(id=data["Team_id"]).first()
    
    if q_team_id is None:
        q_team_id = session.query(Team).filter_by(team_name="Others").first()
    if int(data["Season"][0:2]) in [15,16,17,18,19,20,21]:
        splayer_stat = PlayerStat(
            player_id = q_player_id.id,
            competition_id = q_competition_id.id,
        
            team_id = q_team_id.id,
            season_id = q_season_id.id,
            squad = data["Squad"],
            appearance = int(data["Apperance"]) if data["Apperance"] != "-" else None,
            PPG = ppg_fix(data['PPG']),
            goals = int(data["Goals"]) if data["Goals"] != "-" else None,
            assists = int(data["Assists"]) if (data["Assists"] != "-") and(data["Assists"]) else None,
            own_goal = int(data["Own_goal"]) if data["Own_goal"] != "-" else None,
            sub_off = int(data["Substitutions_off"]) if data["Substitutions_off"] != "-" else None,
            sub_on = int(data["Substitutions_on"]) if data["Substitutions_on"] != "-" else None,
            yellow_card = int(data["Yellow_card"]) if data["Yellow_card"] != "-" else None,
            second_yellow_card = int(data["Second_yellow_card"]) if data["Second_yellow_card"] != "-" else None,
            red_card = int(data["Red_card"]) if data["Red_card"] != "-" else None,
            penalty_goals = int(data["Penalty_goals"]) if (data["Penalty_goals"] != "-") and (data["Penalty_goals"]) else None,
            clean_sheets =int(data["Clean_sheets"]) if (data["Clean_sheets"] != "-") and (data["Clean_sheets"]) else None,
            goal_conceded =int(data["Goals_conceded"]) if (data["Goals_conceded"] != "-") and (data["Goals_conceded"]) else None,
            minutes_per_goal = to_minute(data["Minutes_per_goal"]) if data["Minutes_per_goal"] != "-" else None,
            minutes_play = to_minute(data["Minutes_played"]) if data["Minutes_played"] != "-" else None,
        )
        session.add(splayer_stat)   




# Commit the changes to the database
session.commit()
