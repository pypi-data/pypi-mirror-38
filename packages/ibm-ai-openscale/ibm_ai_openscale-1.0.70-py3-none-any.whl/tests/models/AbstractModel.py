from abc import ABC, abstractmethod


class AbstractModel(ABC):

    @abstractmethod
    def publish_to_wml(self, wml_client):
        pass

    @abstractmethod
    def get_model_props(self, wml_client):
        pass

    @abstractmethod
    def get_scoring_payload(self):
        pass
