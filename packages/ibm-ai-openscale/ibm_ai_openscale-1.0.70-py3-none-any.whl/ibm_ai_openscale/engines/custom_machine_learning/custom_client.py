from ibm_ai_openscale.base_classes.clients import Client
from ibm_ai_openscale.base_classes import Artifact, SourceDeployment
from .consts import CustomConsts
from .asset import CustomMachineLearningAsset
from ibm_ai_openscale.utils import *
import requests
import datetime


class CustomClient(Client):
    service_type = CustomConsts.SERVICE_TYPE

    def __init__(self, binding_uid, service_credentials, project_id=None):
        Client.__init__(self, binding_uid)
        self.url = service_credentials['url']
        self.deployment_endpoint = CustomConsts.DEPLOYMENT_ENDPOINT_PATTERN.format(self.url)
        self.header = {}
        self.username = None
        self.password = None

        if 'username' in service_credentials.keys():
            self.username = service_credentials['username']

        if 'password' in service_credentials.keys():
            self.password = service_credentials['password']

        if 'header' in service_credentials.keys():
            self.header = service_credentials['header']

    def _make_artifact_from_details(self, details):

        return Artifact(
            details['entity']['asset']['guid'],
            details['entity']['scoring_url'],
            self.binding_uid,
            details['entity']['asset']['name'],
            'model',
            details['metadata']['created_at'],
            [],
            details
        )

    def get_artifact(self, source_uid):
        details = self._get_deployments_details()
        asset_details = {}

        for detail in details:
            if detail['metadata']['guid'] == source_uid:
                asset_details = detail

        return self._make_artifact_from_details(asset_details)

    def get_artifacts(self):
        models = self._get_deployments_details()
        unique_models = []
        unique_source_uids = set()

        for model in models:
            model_uid = model['entity']['asset']['guid']
            if model_uid not in unique_source_uids:
                unique_models.append(model)
            unique_source_uids.add(model_uid)

        return [self._make_artifact_from_details(asset) for asset in unique_models]

    def _get_deployments_details(self):
        if self.username is not None and self.password is not None:
            response = requests.get(self.deployment_endpoint, auth=(self.username, self.password), headers=self.header)
        else:
            response = requests.get(self.deployment_endpoint, headers=self.header)

        if response.status_code == 200:
            deployments = response.json()['resources']

        return deployments

    def get_deployments(self, asset=None, deployment_uids=None):
        deployments = self._get_deployments_details()

        if asset is None and deployment_uids is None:
            return [
                SourceDeployment(
                    deployment['metadata']['guid'],
                    deployment['entity']['scoring_url'],
                    deployment['entity']['name'],
                    'online',
                    deployment['metadata']['created_at']
                ) for deployment in deployments
            ]
        elif asset is not None and deployment_uids is None:
            return [
                SourceDeployment(
                    deployment['metadata']['guid'],
                    deployment['entity']['scoring_url'],
                    deployment['entity']['name'],
                    'online',
                    deployment['metadata']['created_at']
                ) for deployment in deployments if deployment['entity']['asset']['guid'] == asset.source_uid
            ]
        elif asset is None and deployment_uids is not None:
            return [
                SourceDeployment(
                    deployment['metadata']['guid'],
                    deployment['entity']['scoring_url'],
                    deployment['entity']['name'],
                    'online',
                    deployment['metadata']['created_at']
                ) for deployment in deployments if deployment['metadata']['guid'] in deployment_uids
            ]
        else:
            return [
                SourceDeployment(
                    deployment['metadata']['guid'],
                    deployment['entity']['scoring_url'],
                    deployment['entity']['name'],
                    'online',
                    deployment['metadata']['created_at']
                ) for deployment in deployments if (deployment['metadata']['guid'] in deployment_uids and deployment['entity']['asset']['guid'] == asset.source_uid)
            ]