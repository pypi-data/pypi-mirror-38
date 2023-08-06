import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models.SPSS import SPSS


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
    
    model = SPSS()

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

    def test_03_bind_wml_instance_and_get_wml_client(self):
        binding_id = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance",
                                                             WatsonMachineLearningInstance(self.wml_credentials))
        self.assertIsNotNone(binding_id)

    def test_04_get_wml_client(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        self.assertIsNotNone(binding_uid)

        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(
            binding_uid)
        self.assertIsNotNone(TestAIOpenScaleClient.wml_client)

    def test_05_store_model(self):
        published_model_details = self.model.publish_to_wml(TestAIOpenScaleClient.wml_client)
        print("Published model details: {}".format(published_model_details))
        self.assertIsNotNone(published_model_details)

        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model_details)
        TestAIOpenScaleClient.logger.info("Published model ID:" + str(TestAIOpenScaleClient.model_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.model_uid)

    def test_06_create_deployment(self):
        deployment_details = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid,
                                                                name="SPSS AIOS Deployment", asynchronous=False)
        print("Deployment details: {}".format(deployment_details))
        self.assertIsNotNone(deployment_details)

        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment_details)
        print("Deployment ID: {}".format(TestAIOpenScaleClient.deployment_uid))
        self.assertIsNotNone(TestAIOpenScaleClient.deployment_uid)

        TestAIOpenScaleClient.scoring_url = self.wml_client.deployments.get_scoring_url(deployment_details)
        self.assertTrue('online' in str(TestAIOpenScaleClient.scoring_url))

    def test_07_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        self.assertIsNotNone(subscription)
        TestAIOpenScaleClient.aios_model_uid = subscription.uid

    def test_08_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(
            TestAIOpenScaleClient.aios_model_uid)
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details before performance monitoring:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            self.assertEqual(configuration['enabled'], False)

    def test_09_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_10_setup_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.enable()
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after performance monitor ON:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            if configuration['type'] == 'performance_monitoring':
                self.assertEqual(configuration['enabled'], True)
            else:
                self.assertEqual(configuration['enabled'], False)

    def test_11_get_performance_monitoring_details(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.get_details()

    def test_12_score(self):
        print("Scoring model.")

        scoring_payload = self.model.get_scoring_payload()

        for i in range(0, 5):
            scores = self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url, payload=scoring_payload)
            self.assertIsNotNone(scores)

        print("Scoring finished. Waining 2 minutes for propagation.")
        import time
        time.sleep(120)

    def test_13_stats_on_performance_monitoring_table(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.performance_monitoring.show_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content(
            format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_14_disable_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.disable()
        subscription_details = TestAIOpenScaleClient.subscription.get_details()
        print("Subscription details after disabling performance monitoring:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            self.assertEqual(configuration['enabled'], False)

    def test_15_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='quality'))
        print(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(
            deployment_uid=TestAIOpenScaleClient.deployment_uid))

        self.assertTrue(
            len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics()['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=TestAIOpenScaleClient.deployment_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=TestAIOpenScaleClient.subscription.uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestAIOpenScaleClient.subscription.source_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='performance')['deployment_metrics'][
                                0]['metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(
            deployment_uid=TestAIOpenScaleClient.deployment_uid)['metrics']) > 0)

    def test_16_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_17_clean(self):
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
        self.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_18_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_19_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
