import re
import requests

import dotenv
from slackbot.bot import respond_to, listen_to

from common.utils import render

dotenv.load()


class MrQueueHelper:

    def make_api_request(self, endpoint, params=None):
        url = dotenv.get('GITLAB_URL') or 'https://gitlab.com/'
        if not url.endswith('/'):
            url = '{}/'.format(url)

        headers = {
            'PRIVATE-TOKEN': dotenv.get('GITLAB_TOKEN')
        }
        api_endpoint = '{url}{endpoint}'.format(
            url=url, endpoint=endpoint
        )

        response = requests.get(api_endpoint, headers=headers, params=params)
        return response.json()

    def get_project_by_name(self, project_name):
        params = {
            'search': project_name
        }
        endpoint = 'api/v4/projects'
        return self.make_api_request(endpoint, params)

    def get_project_mrs(self, project_name):
        projects = self.get_project_by_name(project_name)
        params = {
            'state': 'opened'
        }
        mrs = []
        for project in projects:
            project_id = project['id']
            endpoint = 'api/v4/projects/{}/merge_requests'.format(project_id)
            response = self.make_api_request(endpoint, params)
            mrs.extend(response)
        return mrs

    def get_assigned_mrs(self, project_name):
        mrs = self.get_project_mrs(project_name)
        assigned_mrs = []
        for mr in mrs:
            if not mr['work_in_progress'] and mr['assignee'] is not None:
                assigned_mrs.append({
                    'title': mr['title'],
                    'url': mr['web_url'],
                    'user': mr['author']['name'],
                    'assignee': mr['assignee']['name']
                })
        return assigned_mrs

    def get_unassigned_mrs(self, project_name):
        mrs = self.get_project_mrs(project_name)
        unassigned_mrs = []
        for mr in mrs:
            if not mr['work_in_progress'] and mr['assignee'] is None:
                unassigned_mrs.append({
                    'title': mr['title'],
                    'url': mr['web_url'],
                    'user': mr['author']['name']
                })

        return unassigned_mrs


@listen_to('queue unassigned', re.IGNORECASE)
@respond_to('queue unassigned', re.IGNORECASE)
def queue_unassigned(message):
    message_text_list = message.body['text'].lower().split()
    if len(message_text_list) < 3:
        error = 'Howdy, please enter a project name'
        response = render('mr_queue_response.j2', error=error)
    else:
        project_name = message_text_list[2:]
        helper = MrQueueHelper()
        context = {
            'mrs': helper.get_unassigned_mrs(project_name)
        }
        if context['mrs']:
            response = render('mr_queue_response.j2', context)
        else:
            error = ("Hey there, it is either there is no assigned "
                     "merge requests or you entered a wrong project name.")
            response = render('mr_queue_response.j2', error=error)
    message.reply(response)


@listen_to('queue assigned', re.IGNORECASE)
@respond_to('queue assigned', re.IGNORECASE)
def queue_assigned(message):
    message_text_list = message.body['text'].lower().split()
    if len(message_text_list) < 3:
        error = 'Howdy, please enter a project name'
        response = render('mr_queue_response.j2', error=error)
    else:
        project_name = message_text_list[2:]
        helper = MrQueueHelper()
        context = {
            'mrs': helper.get_assigned_mrs(project_name)
        }
        if context['mrs']:
            response = render('mr_queue_response.j2', context)
        else:
            error = ("Hey there, it is either there is no assigned "
                     "merge requests or you entered a wrong project name.")
            response = render('mr_queue_response.j2', error=error)
    message.reply(response)
