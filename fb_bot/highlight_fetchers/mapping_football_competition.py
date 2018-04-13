# Mapping allowing different names for competitions to be converted to be conform to database naming for competitions
NAME_MAPPING = {
    'carabao cup': 'league cup',
    'turkey cup 1': 'turkish cup',
    'turkey cup': 'turkish cup',
    'champions laegue': 'champions league',
    'international friendlies': 'friendly match',
    'liga sagres': 'primeira liga',
    'turkish super lig': 'super lig',
    'süper lig': 'super lig',
    'taca da liga': 'taça de portugal',
}


# Return the name form the mapping if in it, otherwise return the same competition name
def get_exact_name(team_name):
    name = NAME_MAPPING.get(team_name)

    if not name:
        name = team_name

    return name