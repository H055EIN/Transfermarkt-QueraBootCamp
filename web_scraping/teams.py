from bs4 import BeautifulSoup
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0'}

leagues = ['premier-league','la-liga','serie-a','bundesliga','ligue-1']
res_teams = []
res_players = []
for league in leagues :
    for year in range(2015,2022):
        url = f'https://www.transfermarkt.us/{league}/startseite/wettbewerb/GB1/plus/?saison_id={year}'
        page = requests.get(url,headers=HEADERS).text
        soup = BeautifulSoup(page,'html.parser')
        teams = soup.select('#yw1 .no-border-links a:nth-child(1)')
        for count,team in enumerate(teams):
            data_team = {}
            data_players = {}
            url = f'https://www.transfermarkt.us'+team.get('href')
            page = requests.get(url,headers=HEADERS).text
            soup = BeautifulSoup(page,'html.parser')
            data_team['team_name'] = team.get('title')
            cups = soup.select('.data-header__success-image')
            cups_num = soup.select('.data-header__success-number')
            cups_list = [cup.get('title') for cup in cups]
            cups_num_list = [num.text for num in cups_num]
            data_team['cups'] = [{'cup_name':value,'cup_num':num_value} for value,num_value in zip(cups_list,cups_num_list)]





