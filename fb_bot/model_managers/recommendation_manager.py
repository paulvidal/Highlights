from datetime import datetime

from fb_bot.model_managers import user_manager
from fb_highlights.models import Recommendation


def add_recommendation(user_id, highlights_model):
    user = user_manager.get_user(user_id)
    click_time = datetime.now()

    Recommendation.objects.update_or_create(user=user,
                                            match_id=highlights_model.id,
                                            team1=highlights_model.team1,
                                            score1=highlights_model.score1,
                                            team2=highlights_model.team2,
                                            score2=highlights_model.score2,
                                            match_time=highlights_model.match_time,
                                            click_time=click_time)