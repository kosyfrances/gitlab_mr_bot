import re

from slackbot.bot import respond_to, listen_to

from common.utils import render


@listen_to('mr help', re.IGNORECASE)
def crq_help(message):
    response = render('help_response.j2')
    message.reply(response)


@respond_to('help', re.IGNORECASE)
def help(message):
    response = render('help_response.j2')
    message.reply(response)
