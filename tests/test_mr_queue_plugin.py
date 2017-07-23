from unittest import TestCase
from unittest.mock import patch

from plugins.mr_queue_plugin import (MrQueueHelper, queue_unassigned,
                                     queue_assigned,)
from .faker import fake_creds, FakeClient, FakeMessage
from common.utils import render


def mr_api():
    return [
        {
            'id': 1,
            'project_id': 3,
            'title': 'title1',
            'state': 'opened',
            'author': {'name': 'name1'},
            'web_url': 'http://url/path',
            'assignee': None,
            'work_in_progress': False
        },
        {
            'id': 2,
            'project_id': 4,
            'title': 'title2',
            'state': 'opened',
            'author': {'name': 'name2'},
            'assignee': {'name': 'name3'},
            'web_url': 'http://url/path',
            'work_in_progress': False
        }
    ]


class TestMrQueueHelper(TestCase):

    def setUp(self):
        self.helper = MrQueueHelper()
        self.mr_api = mr_api()

    @patch('plugins.mr_queue_plugin.MrQueueHelper.make_api_request')
    def test_get_project_by_name(self, api_mock):
        api_mock.return_value = []

        projects = self.helper.get_project_by_name('abc')
        self.assertTrue(api_mock.called)

        self.assertEqual(projects, [])

    @patch('plugins.mr_queue_plugin.MrQueueHelper.get_project_by_name')
    @patch('plugins.mr_queue_plugin.MrQueueHelper.make_api_request')
    def test_get_project_mrs(self, api_mock, project_mock):
        api_mock.side_effect = [[self.mr_api[0]], [self.mr_api[1]]]
        project_mock.return_value = [{'id': 1}, {'id': 2}]

        mrs = self.helper.get_project_mrs('abc')

        self.assertTrue(api_mock.called)
        self.assertTrue(project_mock.called)

        self.assertEqual(mrs, self.mr_api)

    @patch('plugins.mr_queue_plugin.MrQueueHelper.get_project_mrs')
    def test_get_assigned_mrs(self, project_mock):
        project_mock.return_value = self.mr_api

        assigned_mrs = self.helper.get_assigned_mrs('abc')
        mr = self.mr_api[1]
        expected = [{
                    'title': mr['title'],
                    'url': mr['web_url'],
                    'user': mr['author']['name'],
                    'assignee': mr['assignee']['name']
                    }]

        self.assertTrue(project_mock.called)

        self.assertEqual(assigned_mrs, expected)

    @patch('plugins.mr_queue_plugin.MrQueueHelper.get_project_mrs')
    def test_get_unassigned_mrs(self, project_mock):
        project_mock.return_value = self.mr_api

        unassigned_mrs = self.helper.get_unassigned_mrs('abc')
        mr = self.mr_api[0]
        expected = [{
                    'title': mr['title'],
                    'url': mr['web_url'],
                    'user': mr['author']['name']
                    }]

        self.assertTrue(project_mock.called)

        self.assertEqual(unassigned_mrs, expected)


class TestQueue(TestCase):

    def setUp(self):
        self.mr_api = mr_api()
        self.client = FakeClient()
        self.unassigned_msg_without_project = {
            'channel': fake_creds['FAKE_CHANNEL'],
            'type': 'message',
            'text': 'mr unassigned'
        }
        self.assigned_msg_without_project = {
            'channel': fake_creds['FAKE_CHANNEL'],
            'type': 'message',
            'text': 'mr assigned'
        }
        self.unassigned_msg_with_project = {
            'channel': fake_creds['FAKE_CHANNEL'],
            'type': 'message',
            'text': 'mr unassigned project1'
        }
        self.assigned_msg_with_project = {
            'channel': fake_creds['FAKE_CHANNEL'],
            'type': 'message',
            'text': 'mr unassigned project2'
        }

        self.unassigned_message_without_project = FakeMessage(
            self.client, self.unassigned_msg_without_project
        )
        self.assigned_message_without_project = FakeMessage(
            self.client, self.assigned_msg_without_project
        )
        self.unassigned_message_with_project = FakeMessage(
            self.client, self.unassigned_msg_with_project
        )
        self.assigned_message_with_project = FakeMessage(
            self.client, self.assigned_msg_with_project
        )

    @patch('slackbot.dispatcher.Message')
    def test_queue_unassigned_without_project_name(self, mock_object):
        mock_object.return_value = self.unassigned_message_without_project
        mock_object.body = self.unassigned_msg_without_project

        queue_unassigned(mock_object)
        error = 'Howdy, please enter a project name'

        self.assertTrue(mock_object.reply.called)
        mock_object.reply.assert_called_with(
            render('mr_queue_response.j2', error=error)
        )

    @patch('slackbot.dispatcher.Message')
    def test_queue_assigned_without_project_name(self, mock_object):
        mock_object.return_value = self.assigned_message_without_project
        mock_object.body = self.assigned_msg_without_project

        queue_assigned(mock_object)
        error = 'Howdy, please enter a project name'

        self.assertTrue(mock_object.reply.called)
        mock_object.reply.assert_called_with(
            render('mr_queue_response.j2', error=error)
        )

    @patch('plugins.mr_queue_plugin.MrQueueHelper.get_unassigned_mrs')
    @patch('slackbot.dispatcher.Message')
    def test_queue_unassigned_with_project_name(self, msg_mock, mr_mock):
        msg_mock.return_value = self.unassigned_message_with_project
        msg_mock.body = self.unassigned_msg_with_project
        mr = self.mr_api[0]
        mr_mock.return_value = {
            'title': mr['title'],
            'url': mr['web_url'],
            'user': mr['author']['name']
        }
        context = {
            'mrs': mr_mock.return_value
        }

        queue_unassigned(msg_mock)

        self.assertTrue(msg_mock.reply.called)
        msg_mock.reply.assert_called_with(
            render('mr_queue_response.j2', context)
        )

    @patch('plugins.mr_queue_plugin.MrQueueHelper.get_assigned_mrs')
    @patch('slackbot.dispatcher.Message')
    def test_queue_assigned_with_project_name(self, msg_mock, mr_mock):
        msg_mock.return_value = self.assigned_message_with_project
        msg_mock.body = self.assigned_msg_with_project
        mr = self.mr_api[1]
        mr_mock.return_value = {
            'title': mr['title'],
            'url': mr['web_url'],
            'user': mr['author']['name'],
            'assignee': mr['assignee']['name']
        }
        context = {
            'mrs': mr_mock.return_value
        }

        queue_assigned(msg_mock)

        self.assertTrue(msg_mock.reply.called)
        msg_mock.reply.assert_called_with(
            render('mr_queue_response.j2', context)
        )

    @patch('plugins.mr_queue_plugin.MrQueueHelper.get_unassigned_mrs')
    @patch('slackbot.dispatcher.Message')
    def test_queue_unassigned_with_wrong_project_name(self, msg_mock, mr_mock):
        msg_mock.return_value = self.unassigned_message_with_project
        msg_mock.body = self.unassigned_msg_with_project
        mr_mock.return_value = []
        error = ("Hey there, it is either there is no assigned "
                 "merge requests or you entered a wrong project name.")

        queue_unassigned(msg_mock)

        self.assertTrue(msg_mock.reply.called)
        msg_mock.reply.assert_called_with(
            render('mr_queue_response.j2', error=error)
        )

    @patch('plugins.mr_queue_plugin.MrQueueHelper.get_assigned_mrs')
    @patch('slackbot.dispatcher.Message')
    def test_queue_assigned_with_wrong_project_name(self, msg_mock, mr_mock):
        msg_mock.return_value = self.assigned_message_with_project
        msg_mock.body = self.assigned_msg_with_project
        mr_mock.return_value = []
        error = ("Hey there, it is either there is no assigned "
                 "merge requests or you entered a wrong project name.")

        queue_assigned(msg_mock)

        self.assertTrue(msg_mock.reply.called)
        msg_mock.reply.assert_called_with(
            render('mr_queue_response.j2', error=error)
        )
