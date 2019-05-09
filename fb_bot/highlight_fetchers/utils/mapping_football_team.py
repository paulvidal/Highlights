import nltk

from fb_bot.model_managers import football_team_mapping_manager


# Return the name from the mapping if in it, otherwise return the same team name
def get_exact_name(team_name):
    name_mapping = football_team_mapping_manager.get_all_football_team_name_mappings()
    name = name_mapping.get(team_name)

    if not name:
        name = team_name

    return name


# Return team names that start the same way as the team name OR are close to the input team name and has first letter in common
def get_similar_names(team_name, all_team_names):
    name_mapping = football_team_mapping_manager.get_all_football_team_name_mappings()
    similar_team_names = []

    # Go through the mapping
    for name in name_mapping:
        if name.startswith(team_name):
            similar_team_names.append(name_mapping[name])

        if team_name[0] == name[0] and nltk.edit_distance(name, team_name) <= 2:
            # If no more than 2 substitution, insertion or deletion are needed to obtain one string starting with the other
            # AND if first letter are the same
            similar_team_names.append(name_mapping[name])

    # Go through all_team_names
    for name in all_team_names:
        if name.startswith(team_name):
            similar_team_names.append(name)

        if team_name[0] == name[0] and nltk.edit_distance(name, team_name) <= 2:
            # If no more than 2 substitution, insertion or deletion are needed to obtain one string starting with the other
            # AND if first letter are the same

            similar_team_names.append(name)

    return similar_team_names