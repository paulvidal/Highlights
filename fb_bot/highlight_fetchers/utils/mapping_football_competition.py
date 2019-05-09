import nltk

from fb_bot.model_managers import football_competition_mapping_manager


# Return the name from the mapping if in it, otherwise return the same competition name
def get_exact_name(competition_name):
    name_mapping = football_competition_mapping_manager.get_all_football_competition_name_mappings()
    name = name_mapping.get(competition_name)

    if not name:
        name = competition_name

    return name


# Return competitions names that start the same way as the competition name OR are close to the input competition name and has first letter in common
def get_similar_names(competition_name, all_competition_names):
    name_mapping = football_competition_mapping_manager.get_all_football_competition_name_mappings()
    similar_competition_names = []

    # Go through the mapping
    for name in name_mapping:
        if name.startswith(competition_name):
            similar_competition_names.append(name_mapping[name])

        if competition_name[0] == name[0] and nltk.edit_distance(name, competition_name) <= 2:
            # If no more than 2 substitution, insertion or deletion are needed to obtain one string starting with the other
            # AND if first letter are the same
            similar_competition_names.append(name_mapping[name])

    # Go through all_competition_names
    for name in all_competition_names:
        if name.startswith(competition_name):
            similar_competition_names.append(name)

        if competition_name[0] == name[0] and nltk.edit_distance(name, competition_name) <= 2:
            # If no more than 2 substitution, insertion or deletion are needed to obtain one string starting with the other
            # AND if first letter are the same
            similar_competition_names.append(name)

    return similar_competition_names