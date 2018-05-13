from datetime import timedelta, datetime

from fb_bot.model_managers import football_team_manager, new_football_registration_manager, football_competition_manager
from fb_highlights.models import LatestHighlight


def get_all_highlights():
    return LatestHighlight.objects.all()


def get_all_highlights_from_source(sources):
    return LatestHighlight.objects.filter(source__in=sources)


def get_all_highlights_without_info():
    return LatestHighlight.objects.filter(video_duration=0)


def get_recent_highlight(minutes):
    return LatestHighlight.objects.filter(
        time_since_added__gt=datetime.today() - timedelta(minutes=minutes)
    )


def get_not_ready_highlights():
    return LatestHighlight.objects.filter(ready=False)


def has_highlight(highlight):
    return LatestHighlight.objects.filter(link=highlight.link)


def increment_click_count(highlight_model):
    highlight_model.click_count += 1
    highlight_model.save()


def get_highlights(team1, score1, team2, score2, date):
    return [h for h in LatestHighlight.objects.filter(team1=team1, team2=team2, score1=score1, score2=score2, valid=True, ready=True)
            if abs(date - h.get_parsed_time_since_added()) < timedelta(days=2)]


def get_similar_sent_highlights(highlight):
    # Add team to new team if does not exists and return
    if not has_teams_in_db(highlight) or not has_competition_in_db(highlight):
        return []

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    return [h for h in LatestHighlight.objects.filter(team1=team1, team2=team2, sent=True)
            if abs(highlight.get_parsed_time_since_added() - h.get_parsed_time_since_added()) < timedelta(days=2) ]


def get_highlights_for_team(team_name):
    if not football_team_manager.has_football_team(team_name):
        return None

    team = football_team_manager.get_football_team(team_name)

    highlights = [highlight for highlight in LatestHighlight.objects.filter(team1=team, valid=True, sent=True)] \
                 + [highlight for highlight in LatestHighlight.objects.filter(team2=team, valid=True, sent=True)]

    return highlights


def get_not_sent_highlights(available_sources):
    return LatestHighlight.objects.filter(sent=False, valid=True, ready=True, source__in=available_sources)


def get_same_highlight_footyroom(highlight_model):
    highlight =[h for h in LatestHighlight.objects.filter(team1=highlight_model.team1, team2=highlight_model.team2, source='footyroom')
                 if abs(highlight_model.get_parsed_time_since_added() - h.get_parsed_time_since_added()) < timedelta(days=2)]

    return highlight[0] if len(highlight) > 0 else None


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
                                             view_count=highlight.view_count, source=highlight.source,
                                             sent=sent, goal_data=highlight.goal_data)


def delete_highlight(highlight_model):
    LatestHighlight.objects.filter(link=highlight_model.link).delete()


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


def set_score(highlight_model, score1, score2):
    highlight_model.score1 = score1
    highlight_model.score2 = score2
    highlight_model.save()


def set_goal_data(highlight_model, goal_data):
    highlight_model.goal_data = goal_data
    highlight_model.save()


def set_ready(highlight_model):
    highlight_model.ready = True
    highlight_model.save()


def convert_highlight(highlight_model, new_link, new_source):
    # create a new highlight with information changed
    LatestHighlight.objects.update_or_create(link=new_link, img_link=highlight_model.img_link,
                                             time_since_added=highlight_model.time_since_added, team1=highlight_model.team1,
                                             score1=highlight_model.score1, team2=highlight_model.team2,
                                             score2=highlight_model.score2, category=highlight_model.category,
                                             view_count=highlight_model.view_count, source=new_source,
                                             sent=highlight_model.sent, ready=False, goal_data=highlight_model.goal_data)


# HELPERS

def has_teams_in_db(highlight):
    return football_team_manager.has_football_team(highlight.team1) and \
           football_team_manager.has_football_team(highlight.team2)


def add_new_team_to_db(highlight):
    if not football_team_manager.has_football_team(highlight.team1):
        new_football_registration_manager.add_football_registration(highlight.team1, highlight.source)

    if not football_team_manager.has_football_team(highlight.team2):
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


def get_similar_highlights(highlight, highlights_model):
    return [h for h in highlights_model if is_same_match_highlight(highlight, h)]


def is_same_match_highlight(h1, h2):
    return h1.team1 == h2.team1 and h1.team2 == h2.team2 \
           and abs(h1.get_parsed_time_since_added() - h2.get_parsed_time_since_added()) < timedelta(days=2)


def get_best_highlight(highlight_models, extended=False):
    """
    Get the most relevant highlight to send to the user (depending on the priority the highlight source)

    :param highlight_models: list of highlights for a match, coming from different sources
    :param extended: parameter to determine if should egt extended highlight or not
    :return: the most relevant highlight (most recent with highest priority)
    """
    current_best = None

    for h in highlight_models:
        if not current_best:
            current_best = h
            continue

        # Priority short-circuiting
        if current_best.priority_short > 0 or h.priority_short > 0:
            current_best = h if h.priority_short > current_best.priority_short else current_best
            continue

        current_best = determine_best_highlight(current_best, h, current_best.score1 + current_best.score2)

    # Extended highlight is always based on the short highlight
    if extended:
        highlight_models_extended = [h for h in highlight_models if current_best.video_duration > 0 and h.video_duration > current_best.video_duration]

        if len(highlight_models_extended) == 0:
            return current_best

        current_best_extended = None

        for h in highlight_models_extended:
            if not current_best_extended:
                current_best_extended = h
                continue

            # Priority short-circuiting
            if current_best_extended.priority_extended > 0 or h.priority_extended > 0:
                current_best_extended = h if h.priority_extended > current_best_extended.priority_extended else current_best_extended
                continue

            current_best_extended = determine_best_highlight_extended(current_best_extended, h, current_best.video_duration)

        return current_best_extended

    return current_best


def determine_best_highlight(h1, h2, total_goals):
    if h1.video_duration > 0 and h2.video_duration > 0:

        # CASE NO GOALS
        if total_goals == 0:
            return choose(h1, h2, [180, 300, 360, 420, 480, 600], min_threshold=30)

        # CASE 1 or 2 GOALS
        elif total_goals <= 2:
            return choose(h1, h2, [240, 360, 420, 480, 600], min_threshold=60)

        # CASE 3 or 4 GOALS
        elif total_goals <= 4:
            return choose(h1, h2, [300, 360, 420, 480, 600], min_threshold=120)

        # CASE 5 or 6 GOALS
        elif total_goals <= 6:
            return choose(h1, h2, [360, 420, 480, 600], min_threshold=200)

        # CASE 7 or more GOALS
        else:
            return choose(h1, h2, [480, 600], min_threshold=300)

    elif h1.video_duration > 0:
        return h1

    elif h2.video_duration > 0:
        return h2

    else:
        # return most recent as might be the most complete
        return h1 if h1.get_parsed_time_since_added() > h2.get_parsed_time_since_added() else h2


def choose(h1, h2, thresholds, min_threshold):
    for threshold in thresholds:
        if h1.video_duration >= min_threshold and h1.video_duration <= threshold and h1.provider_priority() > h2.provider_priority():
            return h1

        elif h2.video_duration >= min_threshold and h2.video_duration <= threshold and h2.provider_priority() > h1.provider_priority():
            return h2

        elif h1.video_duration >= min_threshold and h2.video_duration >= min_threshold \
                and h1.video_duration <= threshold and h2.video_duration <= threshold and h1.provider_priority() == h2.provider_priority():

            if threshold == thresholds[0]:
                return h1 if h1.video_duration >= h2.video_duration else h2
            else:
                return h1 if h1.video_duration <= h2.video_duration else h2

    return h1 if h1.provider_priority() >= h2.provider_priority() else h2


def determine_best_highlight_extended(h1, h2, short_best_highlight_duration):
    if short_best_highlight_duration <= 300:
        max_threshold = 600
    elif short_best_highlight_duration <= 450:
        max_threshold = 900
    else:
        max_threshold = 1200

    return choose_extended(h1, h2, [1100, 1000, 900, 800, 700, 600], max_threshold=max_threshold)


def choose_extended(h1, h2, thresholds, max_threshold):
    for threshold in thresholds:
        if h1.video_duration <= max_threshold and h1.video_duration >= threshold:
            return h1

        elif h2.video_duration <= max_threshold and h2.video_duration >= threshold:
            return h2

        elif h1.video_duration <= max_threshold and h2.video_duration <= max_threshold \
                and h1.video_duration >= threshold and h2.video_duration >= threshold:
            return h1 if h1.video_duration >= h2.video_duration else h2

    return h1 if h1.provider_priority() >= h2.provider_priority() else h2