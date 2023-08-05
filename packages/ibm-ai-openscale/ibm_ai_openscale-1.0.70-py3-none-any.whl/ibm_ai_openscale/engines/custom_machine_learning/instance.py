from ibm_ai_openscale.base_classes.instances import AIInstance
from ibm_ai_openscale.utils import *
from .consts import CustomConsts
import uuid


class CustomMachineLearningInstance(AIInstance):
    """
    Describes Custom Machine Learning instance.

    :param service_credentials: credentials of custom instance (optional)
    :type service_credentials: dict
    """
    def __init__(self, service_credentials=None):
        if service_credentials is not None:
            validate_type(service_credentials, 'service_credentials', dict, False)

        #TODO do we need to validate what is inside credentials ???
        AIInstance.__init__(self, 'custom_instance_id_' + str(uuid.uuid4()), {'url': ''} if service_credentials is None else service_credentials, CustomConsts.SERVICE_TYPE)
