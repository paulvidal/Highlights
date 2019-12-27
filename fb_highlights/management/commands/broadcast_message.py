from fb_bot.messenger_manager import sender, formatter
from fb_bot.messages import *
from fb_bot.model_managers import user_manager
from fb_highlights.management.commands.CustomCommand import CustomCommand


TEXT = """Hey guys,

Unfortunately, this is our first direct message to you, dear football-lovers, but also the last. Against all our efforts and good will, Highlights Bot will have to shut down at the end of 2019, and will be inactive from 2020.

Facebook's guidelines have slowly straightened their control around Messenger Bots such as us, and sadly, we are not able to keep this formidable adventure going longer without breaking any (more 😅) rules, or Facebook's guidelines...
 
We prefer to end things well and take the chance to say goodbye, hoping you will still be able to find some good highlights in the future (maybe not as comfortably though 😁😉).

It's a tough decision...
Highlights Bot, was above all an idea born from the frustration of having to handle shitty highlights game after game, also grew into a concept that developed itself as much as we also develop ourselves through it. We grew with it. For example, when we began, Mbappé was still a virgin 😂.
 
More seriously, it has truly been a pleasure, a joy and a genuine source of pride to deliver you guys automatically with high-quality content all the time (nearly 😅😜). Again, we were proud to come up with user-friendly tools such as the no spoiler mode, or the subscribing to competition parameter.
 
Moreover, Highlights Bot was also and essentially you guys, your passion and you compliments and your feedbacks overall. 
Over the course of 3 years, more than 2000 of you have used our bot and we will end this wonderful journey with close to a 100,000 views. But the best thing was to talk about it all with some of you and hear both your praise and recommendation.

It is really with great sorrow that we have to say goodbye.

And once again, thank you all. We wish you well.
 
Love, pizzas, and football of course. {}{}{}

Paul & Paul-Etienne""".format(EMOJI_HEART, EMOJI_FOOTBALL, EMOJI_HEART)


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'broadcast message'

    def run_task(self, options):
        all_ids = user_manager.get_all_users_id()

        messages = []

        # # image asset id
        # asset_id = 2183629061849013 if settings.is_prod() else 661776840874725
        #
        # messages.append(
        #     formatter.create_image_attachment_from_saved_asset(asset_id)
        # )

        for text in [TEXT]:
            messages.append(
                formatter.create_message(
                    text,
                )
            )

        sender.send_batch_multiple_facebook_messages(all_ids, messages)
