from fb_bot.messages import *
from fb_bot.messenger_manager.formatter import create_message, create_quick_text_reply_message, \
    create_generic_attachment
from fb_bot.messenger_manager.formatter_highlights import highlights_to_json
from fb_bot.messenger_manager.sender import send_facebook_message
from fb_bot.model_managers import latest_highlight_manager, football_team_manager, football_competition_manager, \
    new_football_registration_manager, user_manager


#
#  MESSAGES
#


def send_highlight_message_for_team_or_competition(fb_id, team):
    return send_facebook_message(fb_id, get_highlights_for_team_or_competitions(fb_id, team))


def send_tutorial_message(fb_id, team):
    return send_facebook_message(fb_id, create_message(TUTORIAL_MESSAGE.format(team)))


def send_recommended_team_tutorial_message(fb_id, recommended):
    return send_facebook_message(fb_id, create_quick_text_reply_message(REGISTRATION_RECOMMEND_MESSAGE, recommended[:9] + [OTHER_BUTTON]))


def send_team_not_found_tutorial_message(fb_id):
    return send_facebook_message(fb_id, create_message(REGISTRATION_NOT_FOUND_MESSAGE))


# For TUTORIAL


# FIXME: duplication with real search
def send_tutorial_highlight(fb_id, team_or_competition):
    highlights_team = latest_highlight_manager.get_highlights_for_team(team_or_competition)
    highlights_competition = latest_highlight_manager.get_highlights_for_competition(team_or_competition)

    # TODO: clean this code - check for teams before
    if highlights_team is None and highlights_competition is None:
        highlights = None
    elif highlights_team is None:
        highlights = highlights_competition
    elif highlights_competition is None:
        highlights = highlights_team
    else:
        highlights = highlights_team + highlights_competition

    if highlights == []:
        # Case no highlight found for the team_or_competition, use example such as PSG, Barcelona, Real Madrid, Spain or France
        highlights = latest_highlight_manager.get_highlights_for_team('psg') \
                     + latest_highlight_manager.get_highlights_for_team('barcelona') \
                     + latest_highlight_manager.get_highlights_for_team('real madrid')\
                     + latest_highlight_manager.get_highlights_for_team('spain')\
                     + latest_highlight_manager.get_highlights_for_team('france')

    # Order highlights by date
    highlights = sorted(highlights, key=lambda h: h.get_parsed_time_since_added(), reverse=True)

    # Eliminate duplicates
    highlights = latest_highlight_manager.get_unique_highlights(highlights, max_count=1)

    return send_facebook_message(fb_id, create_generic_attachment(highlights_to_json(fb_id, highlights)))


def has_highlight_for_team(team):
    return latest_highlight_manager.get_highlights_for_team(team)

# FIXME: code duplicated for tutorial
def get_highlights_for_team_or_competitions(fb_id, team_or_competition, highlight_count=10):
    highlights_team = latest_highlight_manager.get_highlights_for_team(team_or_competition)
    highlights_competition = latest_highlight_manager.get_highlights_for_competition(team_or_competition)

    # TODO: clean this code - check for teams before
    if highlights_team is None and highlights_competition is None:
        highlights = None
    elif highlights_team is None:
        highlights = highlights_competition
    elif highlights_competition is None:
        highlights = highlights_team
    else:
        highlights = highlights_team + highlights_competition

    if highlights == []:
        # Case no highlight found for the team_or_competition
        return create_quick_text_reply_message(NO_HIGHLIGHTS_MESSAGE, [SEARCH_AGAIN_HIGHLIGHTS_BUTTON,
                                                                       HELP_BUTTON,
                                                                       CANCEL_BUTTON])

    if not highlights:
        # Case no team_or_competition name matched
        similar_team_or_competition_names = football_team_manager.similar_football_team_names(team_or_competition) \
                                            + football_competition_manager.similar_football_competition_names(team_or_competition)

        # Register wrong search
        new_football_registration_manager.add_football_registration(team_or_competition, 'user')

        # Check if name of team_or_competition was not properly written
        if len(similar_team_or_competition_names) == 0:
            return create_quick_text_reply_message(NO_MATCH_FOUND, [SEARCH_AGAIN_HIGHLIGHTS_BUTTON,
                                                                    HELP_BUTTON,
                                                                    CANCEL_BUTTON])

        elif len(similar_team_or_competition_names) == 1:
            # Case where only one team_or_competition is similar, so send the highlights for this team_or_competition
            # -> error correction as user might have done a typo
            team_or_competition = similar_team_or_competition_names[0]
            return get_highlights_for_team_or_competitions(fb_id, team_or_competition)

        elif len(similar_team_or_competition_names) >= 2:
            similar_team_or_competition_names = [team_name.title() for team_name in similar_team_or_competition_names]
            return create_quick_text_reply_message(NO_MATCH_FOUND_TEAM_RECOMMENDATION, similar_team_or_competition_names[:9]
                                                   + [HELP_BUTTON,
                                                      CANCEL_BUTTON])

    # Order highlights by date
    highlights = sorted(highlights, key=lambda h: h.get_parsed_time_since_added(), reverse=True)

    # Eliminate duplicates
    highlights = latest_highlight_manager.get_unique_highlights(highlights, max_count=10)

    # Check if user has see result activated
    see_result_setting = user_manager.get_see_result_setting(fb_id)

    return create_generic_attachment(highlights_to_json(fb_id, highlights, see_result=see_result_setting))
