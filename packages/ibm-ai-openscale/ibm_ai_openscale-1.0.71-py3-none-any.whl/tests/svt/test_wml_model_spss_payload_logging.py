import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models import SPSSCustomerSatisfaction


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    aios_model_uid = None
    scoring_url = None
    labels = None
    logger = logging.getLogger(__name__)
    ai_client = None
    wml_client = None
    subscription = None
    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(self):

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials,
                                                        schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance",
                                                             WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(
            binding_uid)

    def test_05_1_store_model(self):
        model_meta_props = {
            self.wml_client.repository.ModelMetaNames.NAME: "SPSS customer sample model",
            self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "John Smith",
            self.wml_client.repository.ModelMetaNames.AUTHOR_EMAIL: "js@js.com",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "spss-modeler",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "18.0",
            self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "spss-modeler",
            self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "18.0"
        }
        published_model_details = self.wml_client.repository.store_model(
            model=SPSSCustomerSatisfaction.get_model_data()['path'], meta_props=model_meta_props)
        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model_details)
        TestAIOpenScaleClient.logger.info("Published model ID:" + str(TestAIOpenScaleClient.model_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.model_uid)

    def test_05_2_create_deployment(self):
        deployment_details = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid,
                                                                name="SPSS AIOS Deployment", asynchronous=False)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment_details)
        TestAIOpenScaleClient.scoring_url = self.wml_client.deployments.get_scoring_url(deployment_details)
        self.assertTrue('online' in str(TestAIOpenScaleClient.scoring_url))

    def test_06_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        TestAIOpenScaleClient.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(
            TestAIOpenScaleClient.aios_model_uid)
        print(str(TestAIOpenScaleClient.subscription.get_details()))

    def test_07b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()

    def test_09_get_payload_logging_details(self):
        payload_logging_details = TestAIOpenScaleClient.subscription.payload_logging.get_details()
        print(str(payload_logging_details))

    def test_10_score(self):
        print("Scoring model.")

        scoring_payload = SPSSCustomerSatisfaction.get_scoring_payload()

        self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url, payload=scoring_payload)
        scores = self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url,
                                                   payload=scoring_payload)

        print("Scoring payload: {}".format(scoring_payload))
        print("Scoring result: {}".format(scores))

        self.assertIsNotNone(scores)

        print("Scoring finished. Waining 2 minutes for propagation.")
        import time
        time.sleep(120)

    def test_11_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)

    def test_12_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_13_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_14_clean(self):
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
        self.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_15_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_16_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        # delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
