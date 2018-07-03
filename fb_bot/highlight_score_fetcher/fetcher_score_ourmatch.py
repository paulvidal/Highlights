import json
import time

import re
import requests
from bs4 import BeautifulSoup


# Get goal data from page HTML
def get_goal_data(soup):
    header = soup.find(class_='match_team_header')

    home = soup.find(class_='home').find(class_='spoiler')
    away = soup.find(class_='away').find(class_='spoiler')

    return _extract_goals(home, home=True) \
           + _extract_goals(away, home=False)


def _extract_goals(goal_section, home):
    goals = []

    for goal_list_item in goal_section.find_all('li'):
        goal = goal_list_item.get_text()

        if not goal:
            continue

        # Do not show red cards
        if goal_list_item.find(class_="match-head-red-card"):
            continue

        goal_scorer = goal[:goal.index('(')]

        regex = "\((.*?)\)"
        search_result = re.compile(regex, 0).search(goal)

        goal_elapsed = search_result.groups()[0].split(',')

        for g in goal_elapsed:
            goal_type = 'goal'

            if 'pen' in g:
                goal_type = 'penalty'
                g = g.replace('pen', '').strip()
            elif 'og' in g:
                goal_type = 'own goal'
                g = g.replace('og', '').strip()

            if '+' in g:
                split = g.split('+')
                g = int(split[0]) + int(split[1])

            goals.append({
                'team': 1 if home else 2,
                'player': goal_scorer,
                'elapsed': int(g),
                'goal_type': goal_type
            })

    return goals


if __name__ == "__main__":

    print("\nFetch goals ------------------------------ \n")

    start_time = time.time()

    page = requests.get("http://ourmatch.net/videos/19-06-2018-colombia-vs-japan/")
    soup = BeautifulSoup(page.content, 'html.parser')

    goals = get_goal_data(soup)

    for goal in goals:
        print(goal)

    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")