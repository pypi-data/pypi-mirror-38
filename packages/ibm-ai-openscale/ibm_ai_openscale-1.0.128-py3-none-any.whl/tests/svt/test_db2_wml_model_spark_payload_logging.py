import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models.Spark import GoSales
import requests


class TestAIOpenScaleClient(unittest.TestCase):
    binding_uid = None
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

    model = GoSales()

    @classmethod
    def setUpClass(self):

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.db2_credentials = get_db2_datamart_credentials()
        self.db2_schema = get_db2_schema_name()

        clean_db2_schema(self.db2_credentials, self.db2_schema)

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)
        self.assertIsNotNone(TestAIOpenScaleClient.ai_client)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(db_credentials=self.db2_credentials, schema=get_db2_schema_name())

    def test_03_bind_wml_instance(self):
        TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))
        self.assertIsNotNone(TestAIOpenScaleClient.binding_uid)

    def test_04_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        print("Binding id: {}".format(binding_uid))
        self.assertEqual(binding_uid, TestAIOpenScaleClient.binding_uid)

        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)
        self.assertIsNotNone(TestAIOpenScaleClient.wml_client)

    def test_05_prepare_deployment(self):
        published_model = self.model.publish_to_wml(self.wml_client)
        print("Published model: {}".format(published_model))
        self.assertIsNotNone(published_model)

        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model)
        print("Published model uid: {}".format(TestAIOpenScaleClient.model_uid))

        deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name="Test deployment",
                                                        asynchronous=False)
        print("Deployment: {}".format(deployment))
        self.assertIsNotNone(deployment)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)
        print("Deployment uid: {}".format(TestAIOpenScaleClient.deployment_uid))

    def test_06_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        TestAIOpenScaleClient.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.aios_model_uid)
        print('Subscription details: ' + str(TestAIOpenScaleClient.subscription.get_details()))

    def test_07b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_07c_discovery_endpoint(self):
        ml_gateway_url = self.aios_credentials['url'] + '/v1/ml_instances/{}/deployments?datamart_id={}'.format(TestAIOpenScaleClient.binding_uid, self.aios_credentials['data_mart_id'])
        print("URL: {}".format(ml_gateway_url))
        response = requests.get(ml_gateway_url, headers=TestAIOpenScaleClient.ai_client._get_headers())
        print(response.status_code)
        print(response.json())

    def test_08_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()

    def test_09_get_payload_logging_details(self):
        payload_logging_details = TestAIOpenScaleClient.subscription.payload_logging.get_details()
        print(str(payload_logging_details))

    def test_10_score(self):

        deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = self.model.get_scoring_payload()

        for i in range(0, 5):
            scorings = self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
            self.assertIsNotNone(scorings)

        import time
        print("Waiting 1 minute for propagation.")
        time.sleep(60)

    def test_11a_stats_on_payload_table_from_db2(self):
        tables = list_db2_tables(self.db2_credentials, self.db2_schema)
        payload_table = None
        for table in tables:
            if "Payload" in table:
                payload_table = table

        self.assertIsNotNone(payload_table)
        print("Payload table: {}".format(payload_table))
        table_content = execute_sql_query(""" SELECT * FROM "{}" """.format(payload_table), db2_credentials=self.db2_credentials)
        print(table_content)

        self.assertEqual(len(table_content), 10)

    def test_11_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)

    def test_12_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_13_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_14_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)

    def test_15_clean(self):
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
        self.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_16_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)

    def test_17_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()


if __name__ == '__main__':
    unittest.main()
