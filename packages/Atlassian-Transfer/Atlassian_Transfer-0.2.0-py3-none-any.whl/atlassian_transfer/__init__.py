from datetime import datetime

import requests
from requests_toolbelt import sessions


__version__ = '0.2.0'


class Attachment:

    def __init__(self, name, size, last_modified, url, session=None):
        self.filename = name
        self.size = size
        self.last_modified = datetime.utcfromtimestamp(int(last_modified))
        self.url = url
        if session is None:
            session = requests.Session()
        self._session = session

    def get(self):
        """Return the file content as a string."""
        r = self._session.get(self.url, headers={'Accept': '*/*'})
        return r.content

    def iter_content(self, chunk_size=1024):
        """Return the file content as an iterable stream."""
        r = self._session.get(self.url, stream=True)
        return r.iter_content(chunk_size)


class Transfer:

    def __init__(self, username, token):
        self._session = sessions.BaseUrlSession(
            base_url='https://transfer.atlassian.com')
        self._session.auth = (username, token)

    def list(self, ticket):
        r = self._session.get(f'/api/list/{ticket}')
        data = r.json()
        attachments = []
        for item in data:
            attachment = Attachment(**item, session=self._session)
            attachments.append(attachment)
        return attachments


class FlaskTransfer(Transfer):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if app is not None:
            self.app = app

        self.username = app.config['TRAC_USERNAME']
        self.auth_token = app.config['TRAC_AUTH_TOKEN']
        super().__init__(self.username, self.auth_token)
