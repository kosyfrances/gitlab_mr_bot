import dotenv

from common.utils import render


dotenv.load()

API_TOKEN = dotenv.get('SLACKBOT_API_TOKEN')

DEFAULT_REPLY = render('help_response.j2')

ERRORS_TO = dotenv.get('ERRORS_CHANNEL')

PLUGINS = [
    'plugins'
]
