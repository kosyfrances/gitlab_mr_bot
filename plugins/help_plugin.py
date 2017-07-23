import re

from slackbot.bot import respond_to, listen_to

from common.utils import render


@listen_to('mr help', re.IGNORECASE)
def channel_help(message):
    response = render('help_response.j2')
    message.reply(response)


@respond_to('help', re.IGNORECASE)
def dm_help(message):
    response = render('help_response.j2')
    message.reply(response)
