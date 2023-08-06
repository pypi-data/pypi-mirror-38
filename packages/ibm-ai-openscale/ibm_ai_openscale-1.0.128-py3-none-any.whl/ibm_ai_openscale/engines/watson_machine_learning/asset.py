from ibm_ai_openscale.base_classes.assets import KnownServiceAsset
from ibm_ai_openscale.supporting_classes.enums import InputDataType


class WatsonMachineLearningAsset(KnownServiceAsset):
    """
    Describes Watson Machine Learning asset.

    :param source_uid: WML asset id
    :type source_uid: str
    :param binding_uid: binding_uid of asset (optional)
    :type binding_uid: str
    :param input_data_type: type of input data: ['structured', 'unstructured_image', 'unstructured_text', 'unstructured_audio', 'unstructured_video'] (optional).
    :type input_data_type: str
    """
    def __init__(self, source_uid, binding_uid=None, input_data_type=InputDataType.STRUCTURED):
        KnownServiceAsset.__init__(self, source_uid, binding_uid, input_data_type)
