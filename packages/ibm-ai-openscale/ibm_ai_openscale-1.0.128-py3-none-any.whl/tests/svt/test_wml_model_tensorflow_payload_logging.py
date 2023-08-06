import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models.Tensorflow import Tensorflow


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    scoring_url = None
    labels = None
    logger = logging.getLogger(__name__)
    ai_client = None
    wml_client = None
    subscription = None
    test_uid = str(uuid.uuid4())

    model = Tensorflow()

    @classmethod
    def setUpClass(self):
        TestAIOpenScaleClient.logger.info("Service Instance: setting up credentials")

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)
        self.assertIsNotNone(TestAIOpenScaleClient.ai_client)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml_instance(self):
        binding_id = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("Tensorflow instance", WatsonMachineLearningInstance(self.wml_credentials))
        print("Datamart binding guid: {}".format(binding_id))
        self.assertIsNotNone(binding_id)

    def test_04_get_wml_client(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        self.assertIsNotNone(binding_uid)

        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)
        self.assertIsNotNone(TestAIOpenScaleClient.wml_client)

    def test_05_store_model(self):
        published_model_details = self.model.publish_to_wml(self.wml_client)
        print("Published model details: {}".format(published_model_details))
        self.assertIsNotNone(published_model_details)

        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model_details)
        self.assertIsNotNone(TestAIOpenScaleClient.model_uid)
        print("Published model ID: {}".format(TestAIOpenScaleClient.model_uid))

    def test_06_create_deployment(self):
        deployment_details = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid, name="Tensorflow payload deployment", asynchronous=False)
        print("Deployment details: {}".format(deployment_details))
        self.assertIsNotNone(deployment_details)

        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment_details)
        print("Deployment uid: {}".format(TestAIOpenScaleClient.deployment_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.deployment_uid)

        TestAIOpenScaleClient.scoring_url = self.wml_client.deployments.get_scoring_url(deployment_details)
        self.assertTrue('online' in str(TestAIOpenScaleClient.scoring_url))

    def test_07_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        TestAIOpenScaleClient.subscription_uid = subscription.uid

        print("Subscription ID: {}".format(TestAIOpenScaleClient.subscription_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.subscription_uid)

    def test_08_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details before performance monitoring:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            self.assertEqual(configuration['enabled'], False)

    def test_09_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_10_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after performance monitor ON:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            if configuration['type'] == 'payload_logging':
                self.assertEqual(configuration['enabled'], True)
            else:
                self.assertEqual(configuration['enabled'], False)

    def test_11_get_payload_logging_details(self):
        TestAIOpenScaleClient.subscription.payload_logging.get_details()

    def test_12_score(self):

        scoring_payload = self.model.get_scoring_payload()

        for i in range(0, 5):
            scores = self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url,
                                                       payload=scoring_payload)
            self.assertIsNotNone(scores)

        import time
        time.sleep(10)

    def test_13_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        payload_logging = TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python')
        self.assertTrue(len(payload_logging['values']) > 0)

    def test_14_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after disabling performance monitoring:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            self.assertEqual(configuration['enabled'], False)

    def test_15_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_16_clean(self):
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
        self.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_17_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_18_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
