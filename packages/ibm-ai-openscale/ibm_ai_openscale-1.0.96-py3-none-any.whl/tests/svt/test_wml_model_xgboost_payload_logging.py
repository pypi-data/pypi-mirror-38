import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models.XGboost import XGBoost


class TestAIOpenScaleClient(unittest.TestCase):
    ai_client = None
    binding_id = None
    subscription = None
    subscription_uid = None

    deployment_uid = None
    model_uid = None
    aios_model_uid = None
    scoring_url = None
    labels = None
    logger = logging.getLogger(__name__)
    wml_client = None
    test_uid = str(uuid.uuid4())

    model = XGBoost()

    @classmethod
    def setUpClass(self):

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)
        self.assertIsNotNone(TestAIOpenScaleClient.ai_client)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml(self):
        TestAIOpenScaleClient.binding_id = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("Xgboost payload instance", WatsonMachineLearningInstance(self.wml_credentials))
        print("Datamart binding guid: {}".format(TestAIOpenScaleClient.binding_id))
        self.assertIsNotNone(TestAIOpenScaleClient.binding_id)

    def test_04_get_binding_id(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        print("Datamart details binding guid: {}".format(binding_uid))
        self.assertIsNotNone(binding_uid)
        self.assertEqual(binding_uid, TestAIOpenScaleClient.binding_id)

    def test_05_get_wml_client(self):
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(TestAIOpenScaleClient.binding_id)
        self.assertIsNotNone(TestAIOpenScaleClient.wml_client)

    def test_06_store_model(self):
        published_model_details = self.model.publish_to_wml(TestAIOpenScaleClient.wml_client)
        print("Published model details: {}".format(published_model_details))

        TestAIOpenScaleClient.model_uid = TestAIOpenScaleClient.wml_client.repository.get_model_uid(published_model_details)
        print("Published model ID: {}".format(TestAIOpenScaleClient.model_uid))

        self.assertIsNotNone(TestAIOpenScaleClient.model_uid)

    def test_07_create_deployment(self):
        deployment_details = TestAIOpenScaleClient.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid, name="XGboost AIOS Payload Dep", asynchronous=False)
        print("Deployment details: {}".format(deployment_details))
        self.assertIsNotNone(deployment_details)

        TestAIOpenScaleClient.deployment_uid = TestAIOpenScaleClient.wml_client.deployments.get_uid(deployment_details)
        print("Deployment ID: {}".format(TestAIOpenScaleClient.deployment_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.deployment_uid)

        TestAIOpenScaleClient.scoring_url = TestAIOpenScaleClient.wml_client.deployments.get_scoring_url(deployment_details)
        print("Scoring url: {}".format(TestAIOpenScaleClient.scoring_url))
        self.assertTrue('online' in str(TestAIOpenScaleClient.scoring_url))

    def test_08_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription ID: {}".format(TestAIOpenScaleClient.subscription_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.subscription_uid)

    def test_09_get_subscription(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        self.assertIsNotNone(TestAIOpenScaleClient.subscription)

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details before payload logging:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            self.assertEqual(configuration['enabled'], False)

    def test_10_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after payload logging ON:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            if configuration['type'] == 'payload_logging':
                self.assertEqual(configuration['enabled'], True)
            else:
                self.assertEqual(configuration['enabled'], False)

    def test_11_get_payload_logging_details(self):
        payload_logging_details = TestAIOpenScaleClient.subscription.payload_logging.get_details()
        print("Payload logging details:\n{}".format(payload_logging_details))

        self.assertIsNotNone(payload_logging_details)
        self.assertEqual(payload_logging_details['enabled'], True)

    def test_12_score(self):
        print("Scoring model ...")

        scoring_data = self.model.get_scoring_payload()

        for i in range(0, 5):
            scores = TestAIOpenScaleClient.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url, payload=scoring_data)
            self.assertIsNotNone(scores)

        import time

        print("Scoring completed. Waiting 2 minutes for propagation.")
        time.sleep(120)

    def test_13_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        payload_logging = TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python')
        self.assertTrue(len(payload_logging['values']) > 0)

    def test_14_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_15_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_16_clean(self):
        TestAIOpenScaleClient.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
        TestAIOpenScaleClient.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_17_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_18_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
