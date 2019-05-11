from datetime import timedelta, datetime

from django.db.models import Q, Min, Sum

from fb_bot.highlight_fetchers.info import sources, providers
from fb_bot.highlight_fetchers.utils import mapping_football_team, mapping_football_competition
from fb_bot.model_managers import football_team_manager, new_football_registration_manager, football_competition_manager
from fb_highlights.models import LatestHighlight

MIN_MINUTES_TO_SEND_HIGHLIGHTS = 20


def get_highlight(link):
    return LatestHighlight.objects.filter(
        link=link
    )[0]


def get_all_highlights():
    return LatestHighlight.objects.all()


def get_all_valid_highlights():
    return LatestHighlight.objects.filter(
        valid=True
    )

def get_all_highlights_from_source(sources):
    return LatestHighlight.objects.filter(
        source__in=sources
    )


def get_all_highlights_without_info():
    return LatestHighlight.objects.filter(
        video_duration=0
    )


def get_recent_highlights(hours=0, minutes=0):
    return LatestHighlight.objects.filter(
        time_since_added__gt=datetime.today() - timedelta(hours=hours, minutes=minutes)
    )


def get_recent_valid_highlights(hours=0, minutes=0):
    return LatestHighlight.objects.filter(
        time_since_added__gt=datetime.today() - timedelta(hours=hours, minutes=minutes),
        valid=True
    )


def get_not_ready_highlights():
    return LatestHighlight.objects.filter(
        ready=False
    )


def has_highlight(highlight):
    return LatestHighlight.objects.filter(
        link=highlight.link
    )


def get_new_id():
    values = LatestHighlight.objects.values('id').order_by('-id')
    return values[0]['id'] + 1 if values else 1


def get_recent_highlights_with_incomplete_infos():
    return LatestHighlight.objects.filter(
        (
            Q(score1=-1) |
            Q(score2=-1) |
            Q(goal_data=[]) |
            ~Q(img_link__contains='ourmatch')
        ) &
        Q(time_since_added__gt=datetime.today() - timedelta(hours=120))
    )


def get_recent_unique_highlights(count=10, search=None):
    highlights = LatestHighlight.objects \
        .filter(
            Q(priority_short__gt=0)
            | Q(time_since_added__lt=datetime.today() - timedelta(minutes=MIN_MINUTES_TO_SEND_HIGHLIGHTS))
        ) \
        .values('id', 'match_time','team1', 'score1', 'team2', 'score2', 'category') \
        .annotate(img_link=Min('img_link'), view_count=Sum('click_count')) \
        .order_by('-match_time', '-view_count', 'team1')

    if search:
        highlights = highlights.filter(
            Q(team1=search)
            | Q(team2=search)
            | Q(category=search)
        )

    return list(highlights[:count])


#
#  Main methods for getting highlights to send
#


# searching highlight to show and redirect to when user clicks
def get_highlights(team1, score1, team2, score2, date):
    if not has_team(team1) or not has_team(team2):
        return None

    team1 = football_team_manager.get_football_team(team1)
    team2 = football_team_manager.get_football_team(team2)

    return LatestHighlight.objects.filter(team1=team1,
                                          team2=team2,
                                          score1=score1,
                                          score2=score2,
                                          valid=True,
                                          ready=True,
                                          source__in=sources.get_available_sources(),
                                          time_since_added__gt=date - timedelta(days=3),
                                          time_since_added__lt=date + timedelta(days=3))


# searching highlight to show using id
def get_highlights_by_id(id):
    return LatestHighlight.objects.filter(id=id,
                                          valid=True,
                                          ready=True,
                                          source__in=sources.get_available_sources())


# searching highlight to show when user makes a search for a team or competition
def get_highlights_for_team_or_competition(team_or_competition_name):
    highlights = []

    # team
    if has_team(team_or_competition_name):
        team = football_team_manager.get_football_team(team_or_competition_name)

        highlights = LatestHighlight.objects.filter(
            Q(team1=team,
              sent=True,
              valid=True,
              ready=True,
              score1__gte=0,
              score2__gte=0,
              source__in=sources.get_available_sources()) |
            Q(team2=team,
              sent=True,
              valid=True,
              ready=True,
              score1__gte=0,
              score2__gte=0,
              source__in=sources.get_available_sources()))\
            .order_by('-match_time', '-time_since_added')

    # competition
    elif has_competition(team_or_competition_name):
        competition = football_competition_manager.get_football_competition(team_or_competition_name)

        highlights = LatestHighlight.objects.filter(category=competition,
                                                    sent=True,
                                                    valid=True,
                                                    ready=True,
                                                    score1__gte=0,
                                                    score2__gte=0,
                                                    source__in=sources.get_available_sources())\
            .order_by('-match_time', '-time_since_added')

    return list(highlights)

#
#  Main methods for getting highlights to send
#


def get_inverted_teams_highlights(highlight):
    # Add team to new team if does not exists and return
    if not has_teams_in_db(highlight) or not has_competition_in_db(highlight):
        return []

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    return LatestHighlight.objects.filter(team1=team2,
                                          team2=team1,
                                          time_since_added__gt=highlight.get_parsed_time_since_added() - timedelta(days=3),
                                          time_since_added__lt=highlight.get_parsed_time_since_added() + timedelta(days=3))


def get_same_highlights(highlight):
    # Add team to new team if does not exists and return
    if not has_teams_in_db(highlight) or not has_competition_in_db(highlight):
        return []

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    return LatestHighlight.objects.filter(team1=team1,
                                          team2=team2,
                                          time_since_added__gt=highlight.get_parsed_time_since_added() - timedelta(days=3),
                                          time_since_added__lt=highlight.get_parsed_time_since_added() + timedelta(days=3))


def get_oldest_same_highlight(highlight):
    # Add team to new team if does not exists and return
    if not has_teams_in_db(highlight) or not has_competition_in_db(highlight):
        return []

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    highlight_models = LatestHighlight.objects.filter(team1=team1,
                                                      team2=team2,
                                                      time_since_added__gt=highlight.get_parsed_time_since_added() - timedelta(days=3),
                                                      time_since_added__lt=highlight.get_parsed_time_since_added() + timedelta(days=3))\
        .order_by('time_since_added')

    return highlight_models[0] if highlight_models else None


def get_same_highlights_sent(highlight):
    # Add team to new team if does not exists and return
    if not has_teams_in_db(highlight) or not has_competition_in_db(highlight):
        return []

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    return LatestHighlight.objects.filter(team1=team1,
                                          team2=team2,
                                          sent=True,
                                          time_since_added__gt=highlight.get_parsed_time_since_added() - timedelta(days=3),
                                          time_since_added__lt=highlight.get_parsed_time_since_added() + timedelta(days=3))


def get_valid_not_sent_highlights(available_sources):
    """
    :param available_sources: sources from which a highlight is valid - if source not listed, exclude the highlight
    :return: a list highlight that can be sent, whith complete information
    """

    return LatestHighlight.objects.filter(
        sent=False,
        valid=True,
        ready=True,
        score1__gte=0,
        score2__gte=0,
        source__in=available_sources
    )


def get_same_highlight_from_sources(highlight_model, sources):
    # Check for sources in order of priority
    for source in sources:
        highlights = LatestHighlight.objects.filter(team1=highlight_model.team1,
                                                    team2=highlight_model.team2,
                                                    source=source,
                                                    time_since_added__gt=highlight_model.get_parsed_time_since_added() - timedelta(days=3),
                                                    time_since_added__lt=highlight_model.get_parsed_time_since_added() + timedelta(days=3))

        if highlights:
            return highlights[0]

    return None


#
#  Adding and deleting
#


def add_highlight(highlight, sent=False):
    # Add team to new team if does not exists and return
    if not has_teams_in_db(highlight):
        add_new_team_to_db(highlight)
        return None

    # Add competition to new competition if does not exists and return
    if not has_competition_in_db(highlight):
        add_new_competition_to_db(highlight)
        return None

    # Run mapping for football team names as team can be named differently
    mapped_team1 = mapping_football_team.get_exact_name(highlight.team1)
    mapped_team2 = mapping_football_team.get_exact_name(highlight.team2)

    team1 = football_team_manager.get_football_team(mapped_team1)
    team2 = football_team_manager.get_football_team(mapped_team2)

    # Run mapping for football competition/category names as they can be named differently
    mapped_competition = mapping_football_competition.get_exact_name(highlight.category)

    category = football_competition_manager.get_football_competition(mapped_competition)

    # Get the match time and id
    match_time = datetime.fromordinal(highlight.time_since_added.date().toordinal())
    id = get_new_id()

    oldest = get_oldest_same_highlight(highlight)

    if oldest:
        match_time = oldest.match_time
        id = oldest.id

    new_highlight, _ = LatestHighlight.objects.update_or_create(id=id,
                                                            link=highlight.link,
                                                            img_link=highlight.img_link,
                                                            time_since_added=highlight.time_since_added,
                                                            match_time=match_time,
                                                            team1=team1,
                                                            score1=highlight.score1,
                                                            team2=team2,
                                                            score2=highlight.score2,
                                                            category=category,
                                                            view_count=highlight.view_count,
                                                            source=highlight.source,
                                                            sent=sent,
                                                            goal_data=highlight.goal_data,
                                                            type=highlight.type)

    return new_highlight


def delete_highlight(highlight_model):
    LatestHighlight.objects.filter(link=highlight_model.link).delete()


#
#  Setters
#

def increment_click_count(highlight_model):
    highlight_model.click_count += 1
    highlight_model.save()


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


def set_teams(highlight_model, team1, team2):
    highlight_model.team1 = team1
    highlight_model.team2 = team2
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


def set_extended_type(highlight_model):
    highlight_model.type = 'extended'
    highlight_model.save()


def swap_home_side(highlight_model, new_id):
    temp_team = highlight_model.team1
    temp_score = highlight_model.score1

    highlight_model.team1 = highlight_model.team2
    highlight_model.team2 = temp_team

    highlight_model.score1 = highlight_model.score2
    highlight_model.score2 = temp_score

    highlight_model.id = new_id

    highlight_model.save()


def convert_highlight(highlight_model, new_link, new_source):
    # create a new highlight with information changed
    LatestHighlight.objects.update_or_create(id=highlight_model.id,
                                             link=new_link,
                                             img_link=highlight_model.img_link,
                                             time_since_added=highlight_model.time_since_added,
                                             team1=highlight_model.team1,
                                             score1=highlight_model.score1,
                                             team2=highlight_model.team2,
                                             score2=highlight_model.score2,
                                             category=highlight_model.category,
                                             view_count=highlight_model.view_count,
                                             source=new_source,
                                             sent=highlight_model.sent,
                                             ready=False,
                                             goal_data=highlight_model.goal_data,
                                             type=highlight_model.type)


#
# HELPERS
#

def has_teams_in_db(highlight):
    return has_team(highlight.team1) and has_team(highlight.team2)


def has_team(team):
    return football_team_manager.has_football_team(team)


def add_new_team_to_db(highlight):
    if not football_team_manager.has_football_team(highlight.team1):
        new_football_registration_manager.add_football_registration(highlight.team1, highlight.source)

    if not football_team_manager.has_football_team(highlight.team2):
        new_football_registration_manager.add_football_registration(highlight.team2, highlight.source)


def has_competition_in_db(highlight):
    return has_competition(highlight.category)


def has_competition(competition):
    return football_competition_manager.has_football_competition(competition)


def add_new_competition_to_db(highlight):
    new_football_registration_manager.add_football_registration(highlight.category, highlight.source)


def get_unique_highlights(highlight_models, max_count=10):
    unique = []

    for h in highlight_models:
        if not get_similar_highlights(h, unique):
            unique.append(h)

        # Do not get more than max_count unique highlights
        if len(unique) >= max_count:
            break

    return unique


def get_similar_highlights(highlight, highlight_models):
    return [h for h in highlight_models if is_same_match_highlight(highlight, h)]


def is_same_match_highlight(h1, h2):
    return h1.team1 == h2.team1 and h1.team2 == h2.team2 \
           and abs(h1.get_parsed_time_since_added() - h2.get_parsed_time_since_added()) < timedelta(days=3)


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

        if h.type == 'extended':
            continue

        current_best = determine_best_highlight(current_best, h, current_best.score1 + current_best.score2)

    # Extended highlight is always based on the short highlight
    if extended:
        highlight_models_extended = [h for h in highlight_models if (0 < current_best.video_duration < h.video_duration < 1200 and h.type == 'extended')
                                                                    or h.priority_extended > 0]

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

            current_best_extended = determine_best_highlight_extended(current_best_extended, h)

        return current_best_extended

    return current_best


def determine_best_highlight(h1, h2, total_goals):
    if h1.source == h2.source and abs(h2.video_duration - h1.video_duration) < 15:
        # choose streamable over other videos in case where videos have the same duration
        return h1 if providers.STREAMABLE in h1.link else h2

    elif h1.source == h2.source:
        # return most recent as might be the most complete if same source
        return h1 if h1.get_parsed_time_since_added() > h2.get_parsed_time_since_added() else h2

    elif h1.video_duration > 0 and h2.video_duration > 0:

        # CASE NO GOALS
        if total_goals == 0:
            return choose(h1, h2, [240, 360, 480, 600], min_threshold=30)

        # CASE 1 or 2 GOALS
        elif total_goals <= 2:
            return choose(h1, h2, [300, 420, 600], min_threshold=60)

        # CASE 3 or 4 GOALS
        elif total_goals <= 4:
            return choose(h1, h2, [360, 480, 600], min_threshold=120)

        # CASE 5 or 6 GOALS
        elif total_goals <= 6:
            return choose(h1, h2, [420, 600], min_threshold=200)

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
        # case where both videos have correct duration but one has a better provider
        if _is_correct_duration(h1.video_duration, min_threshold, threshold) and _is_correct_duration(h2.video_duration, min_threshold, threshold) \
                and h1.provider_priority() > h2.provider_priority():
            return h1

        # case where both videos have correct duration but one has a better provider
        elif _is_correct_duration(h1.video_duration, min_threshold, threshold) and _is_correct_duration(h2.video_duration, min_threshold, threshold) \
                and h1.provider_priority() < h2.provider_priority():
            return h2

        # case where both videos have correct duration and same provider
        elif _is_correct_duration(h1.video_duration, min_threshold, threshold) and _is_correct_duration(h2.video_duration, min_threshold, threshold) \
                and h1.provider_priority() == h2.provider_priority():

            # Return most recently added video if both have same priority
            return h1 if h1.get_parsed_time_since_added() > h2.get_parsed_time_since_added() else h2

        # case where only one video has correct duration
        elif _is_correct_duration(h1.video_duration, min_threshold, threshold):
            return h1

        # case where only one video has correct duration
        elif _is_correct_duration(h2.video_duration, min_threshold, threshold):
            return h2

    # case where both video did not have correct duration
    return h1 if h1.provider_priority() >= h2.provider_priority() else h2


def _is_correct_duration(duration, min_threshold, max_threshold):
    return min_threshold <= duration <= max_threshold


def determine_best_highlight_extended(h1, h2):
    if h1.provider_priority() == h2.provider_priority():
        return h1 if h1.video_duration >= h2.video_duration else h2
    else:
        return h1 if h1.provider_priority() >= h2.provider_priority() else h2