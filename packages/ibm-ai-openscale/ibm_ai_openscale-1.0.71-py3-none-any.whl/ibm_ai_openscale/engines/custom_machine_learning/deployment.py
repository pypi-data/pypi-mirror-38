from ibm_ai_openscale.base_classes.assets import Asset
import uuid


class CustomMachineLearningDeployment(Asset):
    """
    Describes asset for generic engine.

    :param name: name of deployment
    :type name: str
    :param scoring_url: scoring endpoint url
    :type name: str
    :param scoring_header: header required to make scoring request
    :type name: dict
    :param binding_uid: binding_uid of asset (not necessary if only one binding exists)
    :type binding_uid: str
    :param asset_type: type of asset - may be one of ['model', 'function'] (default: model)
    :type asset_type: str
    :param frameworks: frameworks used with asset (optional, only for display purposes, will not be saved in AIOS)
    :type frameworks: list of Framework
    """
    def __init__(self, name, scoring_url, scoring_header=None, asset_type='model', frameworks=[], binding_uid=None):
        Asset.__init__(self, binding_uid)
        self.name = name
        self.source_uid = str(uuid.uuid4())
        self.source_url = None
        self.scoring_url = scoring_url
        self.scoring_header = scoring_header
        self.asset_type = asset_type
        self.frameworks = frameworks
        self.source_entry = None
