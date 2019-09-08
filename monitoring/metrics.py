from datadog import initialize
from highlights import settings
from fb_bot.logger import logger

options = {
    'api_key': settings.get_env_var('DD_API_KEY'),
    'app_key': settings.get_env_var('DD_APP_KEY')
}

initialize(**options, mute=False)

# Use Datadog REST API client
from datadog import api

# Set tags
service = 'test'

if settings.PROD_STATUS == 'prod':
    service = 'highlights-bot'

elif settings.PROD_STATUS == 'staging':
    service = 'highlights-bot-beta'

TAGS = ['service:{}'.format(service)]


def send_metric(name, tags=[], error=False, success=False):
    # Do not send metrics in debug mode
    if settings.DEBUG:
        return

    full_name = 'custom.{}'.format(name)
    alert_type = 'error' if error else ('success' if success else 'info')
    all_tags = TAGS + tags + ['alert_type:{}'.format(alert_type)]

    try:
        r = api.Metric.send(metric=full_name, points=1, tags=all_tags)

        if r.get('status') and r.get('status') != 'ok':
            logger.error("Not ok status while sending metric {} with tags [{}]".format(
                name,
                ', '.join(tags)
            ))
    except:
        logger.error("An error occurred when sending metric {} with tags [{}]".format(
            name,
            ', '.join(tags)
        ))


if __name__ == '__main__':
    send_metric(name='test.metric')
