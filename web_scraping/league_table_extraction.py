import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

leagues = [
    ("https://www.transfermarkt.us/premier-league/tabelle/wettbewerb/GB1?saison_id=", "Premier League"),
    ("https://www.transfermarkt.us/serie-a/tabelle/wettbewerb/IT1?saison_id=", "Serie A"),
    ("https://www.transfermarkt.us/laliga/tabelle/wettbewerb/ES1?saison_id=", "La Liga"),
    ("https://www.transfermarkt.us/bundesliga/tabelle/wettbewerb/L1?saison_id=", "Bundesliga"),
    ("https://www.transfermarkt.us/ligue-1/tabelle/wettbewerb/FR1?saison_id=", "Ligue 1")
]
seasons = range(2015, 2022)
max_retries = 3

for season in seasons:
    for url, league in leagues:
        full_url = f"{url}{season}"
        retries = 0
        success = False

        while retries < max_retries and not success:
            try:
                html_content = requests.get(full_url, headers={'User-Agent': 'Mozilla/5.0',
                                                               "Accept-Language": "en-US,en;q=0.5"}).text
                success = True
            except requests.exceptions.RequestException:
                print(f"Error occurred while making a request. Retrying in 5 seconds...")
                time.sleep(5)
                retries += 1

        if not success:
            print(f"Failed to retrieve data from {full_url}. Skipping...")
            continue

        # Rest of your code for parsing the HTML content and creating the dataframe
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find_all("table")[1]
        headers = [th.text.strip() for th in table.find_all("th")]
        headers[2] = 'Matches'
        rows = []
        for tr in table.find_all("tr")[1:]:
            cells = [td.text.strip() for td in tr.find_all("td")]
            rows.append(cells[1:])  # Exclude the first column (position number)
        df = pd.DataFrame(rows, columns=headers)
        print(df)
        print("\n\n")
