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
    subscription = None
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
        TestAIOpenScaleClient.binding_id = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("Xgboost performance instance", WatsonMachineLearningInstance(self.wml_credentials))
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
        deployment_details = TestAIOpenScaleClient.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid, name="XGboost AIOS Deployment", asynchronous=False)
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
        print("Subscription details before performance monitoring:\n{}".format(subscription_details))

        for configuration in subscription_details['entity']['configurations']:
            self.assertEqual(configuration['enabled'], False)

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
        performance_monitoring_details = TestAIOpenScaleClient.subscription.performance_monitoring.get_details()
        print("Performance monitoring details:\n{}".format(performance_monitoring_details))

        self.assertIsNotNone(performance_monitoring_details)
        self.assertEqual(performance_monitoring_details['enabled'], True)

    def test_12_score(self):
        print("Scoring model ...")

        scoring_data = self.model.get_scoring_payload()

        for i in range(0, 5):
            scores = TestAIOpenScaleClient.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url, payload=scoring_data)
            self.assertIsNotNone(scores)

        import time

        print("Scoring completed. Waiting 2 minutes for propagation.")
        time.sleep(120)

    def test_13_stats_on_performance_monitoring_table(self):
        print("Printing performance table: ")
        TestAIOpenScaleClient.subscription.performance_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.performance_monitoring.show_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content(format='python')
        print("Performance metrics:\n{}".format(performance_metrics))
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_14_disable_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.fairness_monitoring.disable()

    def test_15_get_metrics(self):
        deployment_metrics = TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics()
        deployment_metrics_deployment_uid = TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid)
        deployment_metrics_subscription_uid = TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid)
        deployment_metrics_asset_id = TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid)
        deployment_metrics_quality = TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        performance_metrics = TestAIOpenScaleClient.subscription.performance_monitoring.get_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid)

        print("Deployment metrics:\n{}".format(deployment_metrics))
        print("Deployment metrics deployment uid:\n{}".format(deployment_metrics_deployment_uid))
        print("Deployment metrics subscription uid:\n{}".format(deployment_metrics_subscription_uid))
        print("Deployment metrics asset uid:\n{}".format(deployment_metrics_asset_id))
        print("Deployment metrics quality:\n{}".format(deployment_metrics_quality))
        print("Performance monitoring metrics:\n{}".format(performance_metrics))

        self.assertGreater(len(deployment_metrics), 0)
        self.assertGreater(len(deployment_metrics_deployment_uid), 0)
        self.assertGreater(len(deployment_metrics_subscription_uid), 0)
        self.assertGreater(len(deployment_metrics_asset_id), 0)
        self.assertGreater(len(performance_metrics), 0)

    def test_16_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_17_clean(self):
        TestAIOpenScaleClient.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
        TestAIOpenScaleClient.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_18_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_19_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
