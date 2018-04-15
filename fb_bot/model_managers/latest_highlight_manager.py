from datetime import timedelta

from fb_bot.model_managers import football_team_manager, new_football_registration_manager, football_competition_manager
from fb_highlights.models import LatestHighlight


def get_all_highlights():
    return LatestHighlight.objects.all()


# FIXME: improve query performance
def get_all_highlights_from_source(source):
    return [h for h in LatestHighlight.objects.all() if h.source == source]


def get_all_highlights_without_info():
    return LatestHighlight.objects.filter(video_duration=0)


def has_highlight(highlight):
    return LatestHighlight.objects.filter(link=highlight.link)


def increment_click_count(highlight_model):
    highlight_model.click_count += 1
    highlight_model.save()


def get_highlights(team1, score1, team2, score2, date):
    return [h for h in LatestHighlight.objects.filter(team1=team1, team2=team2, score1=score1, score2=score2, valid=True)
            if abs(date - h.get_parsed_time_since_added()) < timedelta(days=2)]


def get_similar_sent_highlights(highlight):
    # Add team to new team if does not exists and return
    if not has_teams_in_db(highlight) or not has_competition_in_db(highlight):
        return []

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    return [h for h in LatestHighlight.objects.filter(team1=team1, team2=team2, score1=highlight.score1, score2=highlight.score2, sent=True)
            if abs(highlight.get_parsed_time_since_added() - h.get_parsed_time_since_added()) < timedelta(days=2) ]


def get_highlights_for_team(team_name):
    if not football_team_manager.has_football_team(team_name):
        return None

    team = football_team_manager.get_football_team(team_name)

    highlights = [highlight for highlight in LatestHighlight.objects.filter(team1=team, valid=True)] \
                 + [highlight for highlight in LatestHighlight.objects.filter(team2=team, valid=True)]

    return highlights


# Setters

def set_sent(highlight_model):
    highlight_model.sent = True
    highlight_model.save()


def set_invalid(highlight_model):
    highlight_model.valid = False
    highlight_model.save()


def set_img_link(highlight_model, img_link):
    highlight_model.img_link = img_link
    highlight_model.save()


def set_video_duration(highlight_model, duration):
    highlight_model.video_duration = duration
    highlight_model.save()


def set_video_url(highlight_model, video_url):
    highlight_model.video_url = video_url
    highlight_model.save()


def get_not_sent_highlights():
    return LatestHighlight.objects.filter(sent=False, valid=True)


def get_highlight_img_link_from_footyroom(highlight_model):
    highlight =[h for h in LatestHighlight.objects.filter(team1=highlight_model.team1, team2=highlight_model.team2,
                                                           score1=highlight_model.score1, score2=highlight_model.score2,
                                                           source='footyroom')
                 if abs(highlight_model.get_parsed_time_since_added() - h.get_parsed_time_since_added()) < timedelta(days=2)]

    return highlight[0].img_link if len(highlight) > 0 else None


def add_highlight(highlight, sent=False):
    # Add team to new team if does not exists and return
    if not has_teams_in_db(highlight):
        add_new_team_to_db(highlight)
        return

    # Add competition to new competition if does not exists and return
    if not has_competition_in_db(highlight):
        add_new_competition_to_db(highlight)
        return

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    category = football_competition_manager.get_football_competition(highlight.category)

    LatestHighlight.objects.update_or_create(link=highlight.link, img_link=highlight.img_link,
                                                 time_since_added=highlight.time_since_added, team1=team1, score1=highlight.score1,
                                                 team2=team2, score2=highlight.score2, category=category,
                                                 view_count=highlight.view_count, source=highlight.source, sent=sent)


def delete_highlight(highlight_model):
    LatestHighlight.objects.filter(link=highlight_model.link).delete()


# HELPERS

def has_teams_in_db(highlight):
    return football_team_manager.has_football_team(highlight.team1) and \
           football_team_manager.has_football_team(highlight.team2)


def add_new_team_to_db(highlight):
    new_football_registration_manager.add_football_registration(highlight.team1, highlight.source)
    new_football_registration_manager.add_football_registration(highlight.team2, highlight.source)


def has_competition_in_db(highlight):
    return football_competition_manager.has_football_competition(highlight.category)


def add_new_competition_to_db(highlight):
    new_football_registration_manager.add_football_registration(highlight.category, highlight.source)


def get_unique_highlights(highlight_models):
    unique = []

    for h in highlight_models:
        if not get_similar_highlights(h, unique):
            unique.append(h)

    return unique


def get_best_highlight(highlight_models):
    """
    Get the most relevant highlight to send to the user (depending on the priority the highlight source)

    :param highlight_models: list of highlights for a match, coming from different sources
    :return: the most relevant highlight (most recent with highest priority)
    """
    current_best = None

    for h in highlight_models:
        if not current_best:
            current_best = h
            continue

        h_time = h.get_parsed_time_since_added()
        current_best_time = current_best.get_parsed_time_since_added()

        if h.priority() >= current_best.priority():

            if h.priority() > current_best.priority():
                current_best = h
            elif h_time > current_best_time:
                current_best = h

    return current_best


def get_similar_highlights(highlight, highlights_model):
    return [h for h in highlights_model if is_same_match_highlight(highlight, h)]


def is_same_match_highlight(h1, h2):
    return h1.team1 == h2.team1 and h1.team2 == h2.team2 \
           and abs(h1.get_parsed_time_since_added() - h2.get_parsed_time_since_added()) < timedelta(days=2)