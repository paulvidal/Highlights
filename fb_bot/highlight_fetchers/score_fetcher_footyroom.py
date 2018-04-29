import json
import time

import requests
from bs4 import BeautifulSoup

from fb_bot.highlight_fetchers import mapping_football_team


# Get goal data from page HTML
def get_goal_data(soup):
    for script in soup.find_all('script'):
        script_text = script.text

        if 'DataStore.match' in script_text:
            script_text = script_text.strip().replace('DataStore.match = ', '')
            match_data = json.loads(script_text)

            return _extract_goals(match_data)

    return []


def _extract_goals(match_data):
    goals = []

    home_team = match_data["homeTeam"]['name']
    away_team = match_data["awayTeam"]['name']

    incidents = match_data["incidents"]

    i = 0

    while incidents.get(str(i)):
        incident = incidents[str(i)]

        category = incident.get('code').get('category')
        id = incident.get('code').get('id')

        player = incident.get('player').get('name')

        side = incident.get('side')

        elapsed = incident.get('elapsed')

        if category == 'g' and id in ['g', 'p', 'og']: # goal
            goal_type = 'goal'

            if id == 'p':
                goal_type = 'penalty'
            elif id == 'og':
                goal_type = 'own goal'

            goals.append({
                'team': 1 if side == 'home' else 2,
                'player': player,
                'elapsed': elapsed,
                'goal_type': goal_type
            })

        i += 1

    return goals


if __name__ == "__main__":

    print("\nFetch goals ------------------------------ \n")

    start_time = time.time()

    page = requests.get("http://footyroom.com/matches/79950605/liverpool-vs-roma/review")
    soup = BeautifulSoup(page.content, 'html.parser')

    goals = get_goal_data(soup)

    for goal in goals:
        print(goal)

    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")