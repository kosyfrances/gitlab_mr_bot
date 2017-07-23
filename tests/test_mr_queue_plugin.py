from unittest import TestCase
from unittest.mock import patch

from plugins.mr_queue_plugin import MrQueueHelper


class TestMrQueueHelper(TestCase):

    def setUp(self):
        self.helper = MrQueueHelper()
        self.mr_api = [
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
