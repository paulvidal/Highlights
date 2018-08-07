import emoji

#
#  EMOJIS
#

def emo(alias):
    return emoji.emojize(alias, use_aliases=True)


EMOJI_WAVE = emo(':wave:')
EMOJI_MAGNIFYING_GLASS = emo(':mag:')
EMOJI_SUBSCRIPTION = emo(':bell:')
EMOJI_CROSS = emo(':x:')
EMOJI_ADD = emo(':heavy_plus_sign:')
EMOJI_REMOVE = emo(':heavy_minus_sign:')
EMOJI_DONE = emo(':ok_hand:')
EMOJI_HELP = emo(':question:')
EMOJI_FOOTBALL = emo(':soccer:')
EMOJI_ONE = '1)'
EMOJI_TWO = '2)'
EMOJI_SWEAT = emo(':cold_sweat:')
EMOJI_INNOCENT = emo(':innocent:')
EMOJI_HEART = emo(':heart:')
EMOJI_BROKEN_HEART = emo(':broken_heart:')
EMOJI_THUMBS_UP = emo(':+1:')
EMOJI_FIRE = emo(':fire:')
EMOJI_TV = emo(':tv:')
EMOJI_MUSCLE = emo(':muscle:')
EMOJI_CLAP = emo(':clap:')
EMOJI_EXPLOSION = emo(':boom:')
EMOJI_100 = emo(':100:')
EMOJI_WINK = emo(':wink:')
EMOJI_SCREAM = emo(':scream:')
EMOJI_HEART_EYES = emo(':heart_eyes:')
EMOJI_SMILE = emo(':smile:')
EMOJI_UMBRELLA = emo(':umbrella:')
EMOJI_SURPRISED = emo(':open_mouth:')
EMOJI_GRIN = emo(':grin:')
EMOJI_DIZZY_FACE = emo(':dizzy_face:')
EMOJI_TROPHY = emo(':trophy:')
EMOJI_MUSIC = emo(':notes:')
EMOJI_SPEAKER = emo(':loudspeaker:')
EMOJI_ANGRY = emo(':angry:')
EMOJI_CUP_OF_TEA = emo(':coffee:')
EMOJI_RUNNING = emo(":running:")


#
#  MESSAGES
#

HELP_MESSAGE = "Here is what you can ask me:\n\n" \
               + EMOJI_ONE + " Press \"Search highlights\" and I will give you the latest highlights videos for a team or a competition\n\n" \
               + EMOJI_TWO + " Press \"My subscriptions\" to subscribe to teams and competitions, I will then send you highlights videos as soon as the match is over!"

CANCEL_MESSAGE = "Alright let's stop there then :)"

DONE_MESSAGE = "You're good to go!\nI will send you the latest highlights for your subscriptions as soon as videos are available. " + EMOJI_TV

SEARCH_HIGHLIGHTS_MESSAGE = "Tell me for which team or competition should I give you highlight videos? " + EMOJI_TV

NO_HIGHLIGHTS_MESSAGE = "I'm so sorry but I could not find any recent highlight video for your team or competition " + EMOJI_BROKEN_HEART

GET_STARTED_MESSAGE = "Hey {} " + EMOJI_WAVE + "\n\nI am the smart bot that fetches the latest football highlights for you."

GET_STARTED_MESSAGE_2 = "To get started, enter the name of a " + EMOJI_FOOTBALL + " team or competition you would love to subscribe to."

SUBSCRIPTION_MESSAGE = "I am currently sending you the highlights for the following " + EMOJI_FOOTBALL + " subscriptions: \n\n{}\n\nDo you want to ADD or REMOVE a subscription?"

ADD_REGISTRATIONS_MESSAGE = "Tell me the name of the team or competition you want to add " + EMOJI_FIRE

DELETE_REGISTRATION_NOT_FOUND_MESSAGE = "I did not find this team or competition to remove :/ Please choose one of the followings"

DELETE_REGISTRATION_MESSAGE = "Which team or competition do you want to remove?"

REGISTRATION_RECOMMEND_MESSAGE = "I did not find your team or competition" + EMOJI_BROKEN_HEART + " Did you mean?"

REGISTRATION_NOT_FOUND_MESSAGE = "I did not find your team or competition " + EMOJI_BROKEN_HEART + " Try entering the full name."

REGISTRATION_ADDED_MESSAGE = "{} was successfully registered " + EMOJI_THUMBS_UP

REGISTRATION_DELETED_MESSAGE = "{} successfully removed from your subscriptions " + EMOJI_THUMBS_UP

NO_MATCH_FOUND_TEAM_RECOMMENDATION = "I did not find highlights for your team or competition " + EMOJI_BROKEN_HEART + " Did you mean?"

NO_MATCH_FOUND = "I did not find highlights for your team or competition! " + EMOJI_BROKEN_HEART

NO_REGISTRATION_MESSAGE = "-> No team or competition registered"

ERROR_MESSAGE = "I am sorry, but an error occured " + EMOJI_SWEAT

TUTORIAL_MESSAGE = "Awesome " + EMOJI_CLAP * 2 + " I will now send you the latest highlight videos for {} at the end of every match in the following format. Clicking on the message will redirect you to the video " + EMOJI_TV

THANK_YOU = "Don't say thanks! That's my job " + EMOJI_MUSCLE

SEE_RESULT_SETTING_MESSAGE = "Do you want to receive match results/spoiler (score, goal scorers...) along with your highlight messages, or hide them?\n\nCurrently: {}"
SEE_RESULT_YES = 'Showing results'
SEE_RESULT_NO  = 'Hiding results'

SETTING_INVALID_MESSAGE = "Invalid option " + EMOJI_CROSS + " Please choose one of the suggested options."

SETTING_CHANGED_MESSAGE = "Setting successfully changed " + EMOJI_THUMBS_UP

SHARE_INTRODUCTION_MESSAGE = "I'm counting on you to make me grow! " + EMOJI_MUSCLE

#
#  BUTTONS
#

SEARCH_AGAIN_HIGHLIGHTS_BUTTON = EMOJI_MAGNIFYING_GLASS + " Search again"

NEW_SEARCH_HIGHLIGHTS_BUTTON = EMOJI_MAGNIFYING_GLASS + " Search again"

MY_TEAM_BUTTON = EMOJI_SUBSCRIPTION + " My teams"

HELP_BUTTON = EMOJI_HELP + " Help"

ADD_REGISTRATION_BUTTON = EMOJI_ADD + " Add"

REMOVE_REGISTRATION_BUTTON = EMOJI_REMOVE + " Remove"

DONE_REGISTRATION_BUTTON = EMOJI_DONE + " Done"

CANCEL_BUTTON = EMOJI_CROSS + " Cancel"

OTHER_BUTTON = "Other"

TRY_AGAIN_BUTTON = EMOJI_MAGNIFYING_GLASS + " Try again"

I_M_GOOD_BUTTON = "I'm good " + EMOJI_THUMBS_UP

SHOW_BUTTON = "Show"

HIDE_BUTTON = "Hide"

#
#  NEW HIGHLIGHT MESSAGES
#

NEW_HIGHLIGHT_NEUTRAL_MATCH = [
    "Here's a new {} highlight! " + EMOJI_SMILE,
    "Latest highlight from {}! " + EMOJI_SMILE,
    "{} highlight ready! " + EMOJI_SMILE,
    "New highlight for {}! " + EMOJI_TV,
    "Ground Control to {} " + EMOJI_MUSIC,
    "Just prepared you another {} highlight " + EMOJI_SMILE,
    "Latest match in {} " + EMOJI_FOOTBALL,
    "Back to {}! " + EMOJI_SMILE,
    "What's new in {}? " + EMOJI_FOOTBALL,
    "{} strikes again! " + EMOJI_FOOTBALL + EMOJI_100,
    "Did you miss {} today? " + EMOJI_SMILE,
    "It's time for {}! " + EMOJI_FOOTBALL,
    "Check out what just happened in {} " + EMOJI_FOOTBALL,
    "Enjoy this {} highlight! " + EMOJI_SMILE,
    "All you need is {} " + EMOJI_MUSIC,
]

NEW_HIGHLIGHT_LOST_MATCH = [
    "Here's a new {} highlight! " + EMOJI_SMILE,
    "Latest highlight from {}! " + EMOJI_SMILE,
    "What goes on in {}... stays there! " + EMOJI_WINK,
    "{} highlight ready! " + EMOJI_SMILE,
    "New highlight for {}! " + EMOJI_TV,
    "Ground Control to {} " + EMOJI_MUSIC,
    "Just prepared you another {} highlight " + EMOJI_SMILE,
    "Latest match in {} " + EMOJI_FOOTBALL,
    "Back to {}! " + EMOJI_SMILE,
    "What's new in {}? " + EMOJI_FOOTBALL,
    "Rough fixture in {} today... " + EMOJI_FOOTBALL,
    "{} had no mercy today! " + EMOJI_BROKEN_HEART,
    "Let's not mention {} this week " + EMOJI_WINK,
    "It's alright, we'll forget about {} for a bit " + EMOJI_WINK,
    "Jesus, has {} always been that tough? " + EMOJI_SCREAM,
    "Don't blame me, blame {}! " + EMOJI_INNOCENT,
    "Daamn you {}! " + EMOJI_ANGRY,
    "Oops, no one saw that! " + EMOJI_WINK,
    "Guess you'll have to hide for a couple of days..." + EMOJI_SWEAT,
    "Cup of tea to forget about {}? " + EMOJI_CUP_OF_TEA,
    "I waannaa runawaaayyy " + EMOJI_MUSIC + EMOJI_RUNNING,
    "Goodbye my lover... Goodbye {} " + EMOJI_BROKEN_HEART,

]

NEW_HIGHLIGHT_DRAW_MATCH = [
    "Here's a new {} highlight! " + EMOJI_SMILE,
    "Latest highlight from {}! " + EMOJI_SMILE,
    "What goes on in {}... stays there! " + EMOJI_WINK,
    "{} highlight ready! " + EMOJI_SMILE,
    "New highlight for {}! " + EMOJI_TV,
    "Ground Control to {} " + EMOJI_MUSIC,
    "Just prepared you another {} highlight " + EMOJI_SMILE,
    "Latest match in {} " + EMOJI_FOOTBALL,
    "Back to {}! " + EMOJI_SMILE,
    "What's new in {}? " + EMOJI_FOOTBALL,
    "Rough fixture in {} today... " + EMOJI_FOOTBALL,
    "{} had no mercy today! " + EMOJI_FOOTBALL,
    "{} strikes again! " + EMOJI_FOOTBALL + EMOJI_100,
    "Did you miss {} today? " + EMOJI_SMILE,
    "Check out what just happened in {} " + EMOJI_FOOTBALL,
    "Enjoy this {} highlight! " + EMOJI_SMILE,
    "Ground Control to {} " + EMOJI_MUSIC,
    "New highlight for {}! " + EMOJI_TV,
    "{} highlight ready! " + EMOJI_SMILE,
    "Latest performance in {} " + EMOJI_FOOTBALL,
    "All you need is {} " + EMOJI_MUSIC,
    "Back to {}! " + EMOJI_SMILE,
    "{} is calling! " + EMOJI_SPEAKER,
    "What's new in {}? " + EMOJI_FOOTBALL,
    "It's time for {}! " + EMOJI_FOOTBALL,
    "{} made everyone happy today! " + EMOJI_WINK,
]

NEW_HIGHLIGHT_CHAMPIONS_LEAGUE_MESSAGES = [
    "The Chaaaampiooooons " + EMOJI_HEART + EMOJI_MUSIC,
    "Champions League strikes again! " + EMOJI_FOOTBALL + EMOJI_100,
    "Beautiful Champions League night! " + EMOJI_HEART_EYES,
    "Hope you haven't missed Champions League tonight! " + EMOJI_FOOTBALL,
    "Here's the Champions League highlight you've been waiting for! " + EMOJI_TV,
    "Champions League is back! " + EMOJI_HEART_EYES,
    "Brace yourself, it's Champions League " + EMOJI_FIRE,
    "Are you ready for Champions League? " + EMOJI_GRIN,
    "Did I hear... Champioons Leaague?! " + EMOJI_HEART_EYES,
]

NEW_HIGHLIGHT_CHAMPIONS_LEAGUE_LOT_OF_GOALS_MESSAGES = [
    "GOOOAAALLLS! " + EMOJI_FOOTBALL + " What a day in Champions League",
    "Hallelujah! It's raining goals in Champions League " + EMOJI_UMBRELLA,
    "What a match in Champions League " + EMOJI_SURPRISED,
    "Impressive performance today in Champions League " + EMOJI_MUSCLE,
    "What a night for Champions League! " + EMOJI_SCREAM,
    "Some brilliant goals tonight in Champions League! " + EMOJI_100,
    "You rarely see that many goals in Champions League! " + EMOJI_DIZZY_FACE,
]

NEW_HIGHLIGHT_LOT_OF_GOALS_MESSAGES = [
    "GOOOAAALLLS! " + EMOJI_FOOTBALL + " What a day in {}!",
    "Hallelujah! It's raining goals in {} " + EMOJI_UMBRELLA,
    "What a match in {} " + EMOJI_SURPRISED,
    "Impressive performance today in {} " + EMOJI_MUSCLE,
    "What a day for {}! " + EMOJI_SCREAM,
    "Some brilliant goals today in {}! " + EMOJI_100,
    "Spectacular match in {} " + EMOJI_MUSCLE,
    "Many goals scored today in {} " + EMOJI_FOOTBALL,
    "You gotta love {} for these matches " + EMOJI_HEART_EYES,
]

NEW_HIGHLIGHT_MESSAGES = [
    "{} strikes again! " + EMOJI_FOOTBALL + EMOJI_100,
    "What goes on in {}... stays there! " + EMOJI_WINK,
    "Hope you haven't missed {} today! " + EMOJI_FOOTBALL,
    "Here's the {} highlight you've been waiting for! " + EMOJI_TV,
    "Did you miss {} today? " + EMOJI_SMILE,
    "You're gonna like this {} highlight! " + EMOJI_WINK,
    "Check out what just happened in {} " + EMOJI_FOOTBALL,
    "Beautiful {} day! " + EMOJI_HEART_EYES,
    "Enjoy this {} highlight! " + EMOJI_SMILE,
    "It has been a great {} day! " + EMOJI_FIRE,
    "That's {} the way we like it! " + EMOJI_HEART_EYES,
    "Ground Control to {} " + EMOJI_MUSIC,
    "New highlight for {}! " + EMOJI_TV,
    "{} highlight ready! " + EMOJI_SMILE,
    "Latest performance in {} " + EMOJI_FOOTBALL,
    "All you need is {} " + EMOJI_MUSIC,
    "Back to {}! " + EMOJI_SMILE,
    "{} is calling! " + EMOJI_SPEAKER,
    "What's new in {}? " + EMOJI_FOOTBALL,
    "It's time for {}! " + EMOJI_FOOTBALL,
]



