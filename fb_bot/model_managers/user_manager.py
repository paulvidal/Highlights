from fb_bot import user_fetcher
from fb_highlights.models import User


def get_all_users_id():
    return [user.facebook_id for user in User.objects.all()]


def get_user(fb_id):
    if not _is_in_db(fb_id):
        success = _insert_user(fb_id)

        if not success:
            default_user = User.get_default_user(facebook_id=fb_id)
            default_user.save()
            return default_user

    return User.objects.get(facebook_id=fb_id)


def increment_user_message_count(fb_id):
    if not _is_in_db(fb_id):
        return False

    user = get_user(fb_id)
    user.message_count += 1
    user.save()

    return True


def increment_user_highlight_click_count(fb_id):
    if not _is_in_db(fb_id):
        return False

    user = get_user(fb_id)
    user.highlights_click_count += 1
    user.save()

    return True


def _is_in_db(fb_id):
    return User.objects.filter(facebook_id=fb_id)


def _insert_user(fb_id):
    user_info = user_fetcher.get_facebook_user_info(fb_id)

    if not user_info:
        return False

    facebook_id, first_name, last_name, image_url, locale, timezone, gender = user_info

    User.objects.update_or_create(facebook_id=facebook_id,
                                  first_name=first_name,
                                  last_name=last_name,
                                  image_url=image_url,
                                  locale=locale,
                                  timezone=timezone,
                                  gender=gender)

    return True


# User settings

def get_user_ids_see_result_setting_disabled():
    users = User.objects.filter(see_result=False)
    return set([u.facebook_id for u in users])


def get_see_result_setting(fb_id):
    return get_user(fb_id).see_result


def set_see_result_setting(fb_id, see_result):
    user = get_user(fb_id)
    user.see_result = see_result
    user.save()
