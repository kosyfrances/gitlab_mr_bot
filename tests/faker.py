"""
This file holds reusable fake stuff for mocking the tests.
"""

fake_creds = {
    'FAKE_CHANNEL': 'C12942JF92',
}


class FakeClient:
    def __init__(self):
        self.rtm_messages = []

    def rtm_send_message(self, channel, message):
        self.rtm_messages.append((channel, message))


class FakeMessage:
    def __init__(self, client, body):
        self._client = client
        self._body = body

    def reply(self, message):
        # Perhaps a bit unnecessary to do it this way, but it's close to how
        # dispatcher and message actually works
        self._client.rtm_send_message(self._body['channel'], message)
