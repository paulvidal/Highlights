from fb_bot.model_managers import football_competition_manager
from fb_highlights.models import RegistrationCompetition


def get_competitions_for_user(fb_id):
    competitions = RegistrationCompetition.objects.filter(user_id=fb_id)
    return [competition.competition_name.name for competition in competitions]


def get_users_for_competition(competition_name):
    competition = football_competition_manager.get_football_competition(competition_name)
    competitions = RegistrationCompetition.objects.filter(competition_name=competition)
    return [competition.user.facebook_id for competition in competitions]


def add_competition(fb_id, competition_name):
    competition = football_competition_manager.get_football_competition(competition_name)
    RegistrationCompetition.objects.update_or_create(user_id=fb_id, competition_name=competition)


def delete_competition(fb_id, competition_name):
    competition = football_competition_manager.get_football_competition(competition_name)
    RegistrationCompetition.objects.filter(user_id=fb_id, competition_name=competition).delete()
