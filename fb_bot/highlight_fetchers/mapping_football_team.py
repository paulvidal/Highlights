import nltk

# Mapping allowing different names for teams to be converted to be conform to database naming for team names
NAME_MAPPING = {
    'as roma': 'roma',
    'west brom': 'west bromwich albion',
    'verona': 'hellas verona',
    'chievo': 'chievoverona',
    'deportivo': 'deportivo la coruna',
    'betis': 'real betis',
    'psg': 'paris saint germain',
    'paris': 'paris saint germain',
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
    "borussia m'gladbach": 'borussia monchengladbach',
    'monchengladbach': 'borussia monchengladbach',
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
    'celta': 'celta vigo',
    'olympique marseille': 'marseille',
    'olympique de marseille': 'marseille',
    'olympique lyonnais': 'lyon',
    'olympique de lyon': 'lyon',
    'om': 'marseille',
    'ol': 'lyon',
    'aca': 'ajaccio',
    'asm': 'monaco',
    'aja': 'auxerre',
    'bor': 'bordeaux',
    'lil': 'lille',
    'fcn': 'nantes',
    'nic': 'nice',
    'rcl': 'lens',
    'str': 'rennes',
    'stade rennais': 'rennes',
    'se': 'saint etienne',
    'soc': 'sochaux',
    'tfc': 'toulouse',
    'est': 'troyes',
    'wolverhampton wanderers': 'wolverhampton',
    'wolves': 'wolverhampton',
    'sc freiburg': 'freiburg',
    'fc barcelona': 'barcelona',
    'cardiff city': 'cardiff',
    'newport county': 'newport',
    'peterborough united': 'peterborough',
    'yeovil town': 'yeovil',
    'barca': 'barcelona',
    'leicester': 'leicester city',
    'ogc nice': 'nice',
    'equipe de france': 'france',
    'man u': 'manchester united',
    'man city': 'manchester city',
    'spurs': 'tottenham',
    'gunners': 'arsenal',
    'liverpool fc': 'liverpool',
    'lille osc': 'lille',
    'losc': 'lille',
    'losc lille': 'lille',
    'fc nantes': 'nantes',
    'bourg-peronnas': 'bourg peronnas',
    'porto': 'fc porto',
    'man united': 'manchester united',
    'clarets': 'burnley',
    'blues': 'chelsea',
    'pensioners': 'chelsea',
    'eagles': 'crystal palace',
    'toffees': 'everton',
    'tigers': 'hull city',
    'foxes': 'leicester city',
    'reds': 'liverpool',
    'red devils': 'manchester united',
    'citizens': 'manchester city',
    'magpies': 'newcastle united',
    'newcastle': 'newcastle united',
    'saints': 'southampton',
    'potters': 'stoke city',
    'swans': 'swansea',
    'baggies': 'west bromwich albion',
    'hammers': 'west ham',
    'copenhagen': 'fc copenhagen',
    'ostersunds': 'ostersund',
    'ludogorets razgrad': 'ludogorets',
    'kardemir karabuk': 'karabukspor',
    'zwolle': 'pec zwolle',
    'united': 'manchester united',
    'bayern': 'bayern munich',
    'atletico': 'atletico madrid',
    'milan ac': 'ac milan',
    'milan': 'ac milan',
    'los angeles fc': 'los angeles',
    'real': 'real madrid',
    'fc metz': 'metz',
    'bosnia-herzegovina': 'bosnia and herzegovina',
    'n.ireland': 'northern ireland',
    'hannover': 'hannover 96',
    'wigan': 'wigan athletic',
    'west bromw': 'west bromwich albion',
    'plzen': 'viktoria plzen',
    'salzburg': 'red bull salzburg',
    'breda': 'nac breda',
    'den haag': 'ado den haag',
    'heerenveen‎': 'sc heerenveen‎',
    'akhisarspor': 'akhisar belediyespor',
    'dinamo moscow': 'dynamo moscow',
    'venlo': 'vvv-venlo',
    'juve': 'juventus',
    'angers sco': 'angers',
    'sco': 'angers',
    'vitoria guimaraes': 'vitoria',
    'vitoria sc': 'vitoria',
    'vitoria s.c.': 'vitoria',
    'fc schalke 04': 'schalke 04',
    'schalke': 'schalke 04',
    'herbiers': 'les herbiers',
    'les herbiers vf': 'les herbiers',
    '1899 hoffenheim': 'hoffenheim',
    'hamburger': 'hamburger	sv',
    'bayer 04 leverkusen': 'bayer leverkusen',
    'heart of midlothian fc': 'heart of midlothian',
    'birmingham': 'birmingham city',
    'birmingham city fc': 'birmingham city',
    'preston': 'preston north end',
    'preston north': 'preston north end',
    'derby county fc': 'derby county',
    'deportivo alaves': 'alaves',
    'chievo verona': 'chievoverona',
    'la fc': 'los angeles',
}


# Return the name from the mapping if in it, otherwise return the same team name
def get_exact_name(team_name):
    name = NAME_MAPPING.get(team_name)

    if not name:
        name = team_name

    return name


# Return team names that start the same way as the team name OR are close to the input team name and has first letter in common
def get_similar_names(team_name, all_team_names):
    similar_team_names = []

    # Go through the mapping
    for name in NAME_MAPPING:
        if name.startswith(team_name):
            similar_team_names.append(NAME_MAPPING[name])

        if team_name[0] == name[0] and nltk.edit_distance(name, team_name) <= 2:
            # If no more than 2 substitution, insertion or deletion are needed to obtain one string starting with the other
            # AND if first letter are the same
            similar_team_names.append(NAME_MAPPING[name])

    # Go through all_team_names
    for name in all_team_names:
        if name.startswith(team_name):
            similar_team_names.append(name)

        if team_name[0] == name[0] and nltk.edit_distance(name, team_name) <= 2:
            # If no more than 2 substitution, insertion or deletion are needed to obtain one string starting with the other
            # AND if first letter are the same

            similar_team_names.append(name)

    return similar_team_names