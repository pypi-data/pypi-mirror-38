from datetime import datetime
from pathlib import Path

import requests
from requests_toolbelt import sessions


__version__ = '0.1.0'


class Attachment:

    def __init__(self, name, size, last_modified, url):
        self.name = name
        self.size = size
        self.last_modified = datetime.utcfromtimestamp(int(last_modified))
        self.url = url

    def download(self, path='.'):
        download_dir = Path(path)
        download_path = download_dir / self.name
        r = requests.get(self.url, stream=True)
        with open(download_path, 'wb') as handle:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    handle.write(chunk)


class Transfer:

    def __init__(self, username, token):
        self.session = sessions.BaseUrlSession(
            base_url='https://transfer.atlassian.com')
        self.session.auth = (username, token)

    def list(self, ticket):
        r = self.session.get(f'/api/list/{ticket}')
        data = r.json()
        attachments = []
        for item in data:
            attachment = Attachment(**item)
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
