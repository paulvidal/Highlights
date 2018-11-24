# Mapping allowing different names for competitions to be converted to be conform to database naming for competitions
import nltk

NAME_MAPPING = {
    'carabao cup': 'league cup',
    'turkey cup 1': 'turkish cup',
    'turkey cup': 'turkish cup',
    'champions laegue': 'champions league',
    'liga sagres': 'primeira liga',
    'turkish super lig': 'super lig',
    'süper lig': 'super lig',
    'taca da liga': 'taça de portugal',
    'uefa champions league': 'champions league',
    'champions': 'champions league',
    'barclays premier league': 'premier league',
    'english premier league': 'premier league',
    'epl': 'premier league',
    'liga': 'la liga',
    'liga bbva': 'la liga',
    'la liga bbva': 'la liga',
    'friendlies': 'friendly match',
    'club friendlies': 'friendly match',
    'international champions cup 2018': 'friendly match',
    'international champions cup': 'friendly match',
    'international friendlies': 'friendly match',
    'scottish premier league': 'scottish premiership',
    'scottish league': 'scottish premiership',
    'efl championship': 'championship',
    'spl': 'scottish premiership',
    'major league soccer': 'mls',
    'uefa europa league': 'europa league',
    'taca de portugal': 'taça de portugal',
    'dfb pokal': 'dfb-pokal',
    'world cup 2018': 'world cup',
    'world cup highlights': 'world cup',
    'trophee des champions': 'trophée des champions',
    'dutch super cup': 'johan cruyff shield',
    'johan cruijff shield': 'johan cruyff shield',
    'dfl supercup': 'dfl-supercup',
    'supercopa de espana': 'supercopa de españa',
    'uefa nations league': 'nations league',
    'nations league uefa': 'nations league',
    'league of nations': 'nations league',
    'uefa league of nations': 'nations league',
    'english premier league highlights': 'premier league',
    'champions league highlights': 'champions league',
    'league 1': 'ligue 1',
    'africa cup': 'africa cup of nations'
}


# Return the name from the mapping if in it, otherwise return the same competition name
def get_exact_name(competition_name):
    name = NAME_MAPPING.get(competition_name)

    if not name:
        name = competition_name

    return name


# Return competitions names that start the same way as the competition name OR are close to the input competition name and has first letter in common
def get_similar_names(competition_name, all_competition_names):
    similar_competition_names = []

    # Go through the mapping
    for name in NAME_MAPPING:
        if name.startswith(competition_name):
            similar_competition_names.append(NAME_MAPPING[name])

        if competition_name[0] == name[0] and nltk.edit_distance(name, competition_name) <= 2:
            # If no more than 2 substitution, insertion or deletion are needed to obtain one string starting with the other
            # AND if first letter are the same
            similar_competition_names.append(NAME_MAPPING[name])

    # Go through all_competition_names
    for name in all_competition_names:
        if name.startswith(competition_name):
            similar_competition_names.append(name)

        if competition_name[0] == name[0] and nltk.edit_distance(name, competition_name) <= 2:
            # If no more than 2 substitution, insertion or deletion are needed to obtain one string starting with the other
            # AND if first letter are the same
            similar_competition_names.append(name)

    return similar_competition_names