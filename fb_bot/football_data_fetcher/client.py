import requests

TOKEN = "d18a3cb8c8ae449082ee09e51710e1c7"
BASE_URL = "https://api.football-data.org/v2/"

COMPETITION = 'PL'

if __name__ == "__main__":

    # response = requests.get('https://api.football-data.org/v2/competitions/PL/teams',
    #              headers={
    #                  'X-Auth-Token': TOKEN
    #              })
    #
    # teams = response.json()['teams']
    #
    # for t in teams:
    #     print(t['name'], t['id'])

    response = requests.get('https://api.football-data.org/v2/teams/57',
                            headers={
                                'X-Auth-Token': TOKEN
                            })

    teams = response.json()['teams']

    for t in teams:
        print(t['name'], t['id'])