from datetime import timedelta

from fb_bot.model_managers import football_team_manager, new_football_team_manager
from fb_highlights.models import LatestHighlight


def get_all_highlights():
    return LatestHighlight.objects.all()


def get_all_highlights_from_source(source):
    return [h for h in LatestHighlight.objects.all() if h.source == source]


def has_highlight(highlight):
    return LatestHighlight.objects.filter(link=highlight.link)


def get_similar_highlights(highlight_model):
    return [h for h in LatestHighlight.objects.filter(team1=highlight_model.team1, team2=highlight_model.team2,
                                                      score1=highlight_model.score1, score2=highlight_model.score2)
            if abs(highlight_model.get_parsed_time_since_added() - h.get_parsed_time_since_added()) < timedelta(days=2)]


def get_similar_sent_highlights(highlight):
    # Add team to new team if does not exists and return
    if add_new_team_to_db(highlight):
        return []

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    return [h for h in LatestHighlight.objects.filter(team1=team1, team2=team2, score1=highlight.score1, score2=highlight.score2, sent=True)
            if abs(highlight.get_parsed_time_since_added() - h.get_parsed_time_since_added()) < timedelta(days=2) ]


def get_highlights_for_team(team_name, source):
    if not football_team_manager.has_football_team(team_name):
        return None

    team = football_team_manager.get_football_team(team_name)

    highlights = [highlight for highlight in LatestHighlight.objects.filter(team1=team, source=source)] \
                 + [highlight for highlight in LatestHighlight.objects.filter(team2=team, source=source)]

    return highlights


def set_sent(highlight_model):
    highlight_model.sent = True
    highlight_model.save()


def set_img_link(highlight_model, img_link):
    highlight_model.img_link = img_link
    highlight_model.save()


def get_not_sent_highlights():
    return LatestHighlight.objects.filter(sent=False)


def get_highlight_img_link_from_footyroom(highlight_model):
    highlight =[h for h in LatestHighlight.objects.filter(team1=highlight_model.team1, team2=highlight_model.team2,
                                                           score1=highlight_model.score1, score2=highlight_model.score2,
                                                           source='footyroom')
                 if abs(highlight_model.get_parsed_time_since_added() - h.get_parsed_time_since_added()) < timedelta(days=2)]

    return highlight[0].img_link if len(highlight) > 0 else None


def add_highlight(highlight, sent=False):
    # Add team to new team if does not exists and return
    if add_new_team_to_db(highlight):
        return

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    # check if match for source exists in db
    highlights_in_db = [h for h in LatestHighlight.objects.filter(team1=team1, team2=team2,
                                                                  score1=highlight.score1, score2=highlight.score2,
                                                                  source=highlight.source)
                 if abs(highlight.get_parsed_time_since_added() - h.get_parsed_time_since_added()) < timedelta(days=2)]

    # update link if in db, otherwise insert new highlight
    if highlights_in_db:
        h = highlights_in_db[0]
        h.link = highlight.link
        h.save()

    else:
        LatestHighlight.objects.update_or_create(link=highlight.link, img_link=highlight.img_link,
                                                 time_since_added=highlight.time_since_added, team1=team1, score1=highlight.score1,
                                                 team2=team2, score2=highlight.score2, category=highlight.category,
                                                 view_count=highlight.view_count, source=highlight.source, sent=sent)


def delete_highlight(highlight_model):
    LatestHighlight.objects.filter(link=highlight_model.link).delete()


# HELPERS

def add_new_team_to_db(highlight):
    if not football_team_manager.has_football_team(highlight.team1):
        new_football_team_manager.add_football_team(highlight.team1, highlight.source)
        return True

    if not football_team_manager.has_football_team(highlight.team2):
        new_football_team_manager.add_football_team(highlight.team2, highlight.source)
        return True

    return False

def has_higher_priority_highlight(highlight, not_sent_highlights):
    """
    Check if higher priority in similar highlights exists

    :return: False if there exists a highlight in not_sent_highlight with higher priority than highlight

    Highlights priority:
    1. Hoofoot
    2. Footyroom
    """
    for h in not_sent_highlights:
        if is_same_match_highlight(highlight, h):

            # same match
            if highlight.source == h.source:
                continue

            if h.source == 'hoofoot':
                return True

    return False


def is_same_match_highlight(h1, h2):
    return h1.team1 == h2.team1 and h1.team2 == h2.team2 \
           and abs(h1.get_parsed_time_since_added() - h2.get_parsed_time_since_added()) < timedelta(days=2)