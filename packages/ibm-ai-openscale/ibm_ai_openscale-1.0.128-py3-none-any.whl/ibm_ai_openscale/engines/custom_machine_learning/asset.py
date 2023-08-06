from ibm_ai_openscale.base_classes.assets import KnownServiceAsset


class CustomMachineLearningAsset(KnownServiceAsset):
    """
    Describes Watson Machine Learning asset.

    :param source_uid: asset id
    :type source_uid: str
    :param binding_uid: binding_uid of asset (optional)
    :type binding_uid: str
    """
    def __init__(self, source_uid, binding_uid=None):
        KnownServiceAsset.__init__(self, source_uid, binding_uid)