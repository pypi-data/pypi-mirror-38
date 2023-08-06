class SourceDeployment:
    def __init__(self, guid, url, name, deployment_type, created, scoring_url=None, scoring_authorization=None, scoring_headers=None):
        self.guid = guid
        self.url = url
        self.name = name
        self.deployment_type = deployment_type
        self.created = created
        self.scoring_url = scoring_url
        self.scoring_headers = scoring_headers
        self.scoring_authorization = scoring_authorization

        if self.scoring_url is None:
            self.scoring_url = ''

        if self.scoring_authorization is None:
            self.scoring_authorization = {'method': '', 'credentials': {}}

        if self.scoring_headers is None:
            self.scoring_headers = {}

    def _to_json(self):
        return {
            "deployment_id": self.guid,
            "url": self.url,
            "name": self.name,
            "deployment_type": self.deployment_type,
            "created_at": self.created,
            'scoring_endpoint': {
                'url': self.scoring_url,
                'request_headers': self.scoring_headers,
                'authorization': self.scoring_authorization
            },
        }
