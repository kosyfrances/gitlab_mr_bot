from unittest import TestCase
from unittest.mock import patch

from plugins import help_plugin
from .faker import fake_creds, FakeClient, FakeMessage
from common.utils import render


class TestHelpFunction(TestCase):

    client = FakeClient()
    help_msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'help'
    }

    wrong_msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'bla bla bla'
    }

    channel_msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'mr help'
    }

    wrong_channel_msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'bla bla bla'
    }

    help_message = FakeMessage(client, help_msg)
    wrong_message = FakeMessage(client, wrong_msg)
    channel_message = FakeMessage(client, channel_msg)
    wrong_channel_message = FakeMessage(client, wrong_channel_msg)

    @patch('slackbot.dispatcher.Message', return_value=help_message)
    def test_dm_help_with_help_message(self, mock_object):
        mock_object.body = self.help_msg
        help_plugin.help(mock_object)

        self.assertTrue(mock_object.reply.called)
        mock_object.reply.assert_called_with(render('help_response.j2'))

    @patch('slackbot.dispatcher.Message', return_value=wrong_message)
    def test_dm_help_with_wrong_message(self, mock_object):
        mock_object.body = self.wrong_msg
        help_plugin.help(mock_object)

        self.assertTrue(mock_object.reply.called)
        mock_object.reply.assert_called_with(render('help_response.j2'))

    @patch('slackbot.dispatcher.Message', return_value=channel_message)
    def test_help_message_for_channel(self, mock_object):
        mock_object.body = self.channel_msg
        help_plugin.help(mock_object)

        self.assertTrue(mock_object.reply.called)
        mock_object.reply.assert_called_with(render('help_response.j2'))

    @patch('slackbot.dispatcher.Message', return_value=wrong_channel_message)
    def test_wrong_help_message_for_channel(self, mock_object):
        mock_object.body = self.wrong_channel_msg
        help_plugin.help(mock_object)

        self.assertTrue(mock_object.reply.called)
        mock_object.reply.assert_called_with(render('help_response.j2'))
