# Mapping allowing different names for teams to be converted to be conform to database naming for team names

NAME_MAPPING = {
    'as roma': 'roma',
    'west brom': 'west bromwich albion',
    'verona': 'hellas verona',
    'chievo': 'chievoverona',
    'deportivo': 'deportivo la coruna',
    'betis': 'real betis',
    'psg': 'paris saint germain',
    'as monaco': 'monaco',
    'fc köln': 'fc cologne',
    'fc koln': 'fc cologne',
    'rb leipzig': 'leipzig',
    'stuttgart': 'vfb stuttgart',
    'psv': 'psv eindhoven',
    'sm caen': 'caen',
    'pordenone': 'pordenone calcio',
    'frankfurt': 'eintracht frankfurt',
    'afc bournemouth': 'bournemouth',
    'west ham united': 'west ham',
    'tottenham hotspur': 'tottenham',
    'ssc napoli': 'napoli',
    'brighton & hove albion': 'brighton',
    'huddersfield town': 'huddersfield',
    'inter': 'inter milan',
    'borussia dortmund': 'dortmund',
    'borussia monchengladbach': 'monchengladbach',
    'rasenballsport leipzig': 'leipzig',
    'saint-etienne': 'saint etienne',
    'swansea city': 'swansea',
    'al-jazira': 'al jazira',
    'fc groningen': 'groningen',
    'akhisar belediye genclik ve spor': 'akhisar genclik spor',
    'leeds': 'leeds united',
    'waregem': 'zulte waregem',
    'zulte-waregem': 'zulte waregem',
    'zenit st. petersburg': 'zenit st petersburg',
    'zenit': 'zenit st petersburg',
    'appolon fc': 'apollon limassol',
    'hnk rijeka': 'rijeka',
    'fc twente': 'twente',
    'real murcia': 'murcia',
    'roda jc kerkrade': 'roda',
    'roda jc': 'roda',
    'hamburg': 'hamburger sv',
    'qarabag': 'qarabag fk',
    'sporting': 'sporting cp',
    'formentera': 'sd formentera',
    'celta': 'celta vigo'
}


def is_similar_to_name_in_mapping(team_name):
    for name in NAME_MAPPING:
        if name.startswith(team_name):
            return True

    return False


def get_similar_names_in_mapping(team_name):
    team_names = []

    for name in NAME_MAPPING:
        if name.startswith(team_name):
            team_names.append(NAME_MAPPING[name])

    return team_names


# Return the name form the mapping if in it, otherwise return the same team name
def get_exact_name(team_name):
    name = NAME_MAPPING.get(team_name)

    if not name:
        name = team_name

    return name
