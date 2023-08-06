import unittest
from random import randint

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import *
from preparation_and_cleaning import *


@unittest.skip("Rework on generic needed")
class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    subscription_uid = None
    binding_uid = None
    scoring_url = None
    labels = None
    logger = logging.getLogger(__name__)
    ai_client = None
    wml_client = None
    subscription = None
    test_uid = str(uuid.uuid4())

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

    def test_03_bind_generic(self):
        TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My Generic instance", GenericMachineLearningInstance())
        self.assertIsNotNone(TestAIOpenScaleClient.binding_uid)

    def test_04_get_binding_details(self):
        binding_details = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details(TestAIOpenScaleClient.binding_uid)
        print("Binding details: {}".format(binding_details))
        self.assertIsNotNone(binding_details)
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()

    def test_05_subscribe_generic(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(GenericAsset(name='Product Line on Generic', binding_uid=TestAIOpenScaleClient.binding_uid))
        self.assertIsNotNone(subscription)
        TestAIOpenScaleClient.subscription_uid = subscription.uid
        print("Subscription id: {}".format(TestAIOpenScaleClient.subscription_uid))

    def test_06_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.subscription_uid)
        self.assertIsNotNone(TestAIOpenScaleClient.subscription)
        subscription_detais = TestAIOpenScaleClient.subscription.get_details()
        print('Subscription details: {}'.format(subscription_detais))

    def test_07_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()

    def test_09_setup_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.enable()

    def test_10_get_payload_logging_details(self):
        payload_logging_details = TestAIOpenScaleClient.subscription.payload_logging.get_details()
        print('Payload logging details: {}'.format(payload_logging_details))

    def test_11_get_performance_monitoring_details(self):
        performance_monitoring_details = TestAIOpenScaleClient.subscription.performance_monitoring.get_details()
        print(performance_monitoring_details)

    def test_12_log_payload_record(self):
        input_data = {
            "fields": [
                "GENDER",
                "AGE",
                "MARITAL_STATUS",
                "PROFESSION",
                'PRODUCT_LINE'
            ],
            "values": [["M", 27, "Single", "Professional", "Personal Accessories"]]
        }

        output_data = {
            "fields": [
                "prediction",
                "probability"
            ],
            "values": [["camping equipment", 0.7205234335053059]]

        }

        TestAIOpenScaleClient.subscription.payload_logging.store(request=input_data, response=output_data, response_time=12)

    def test_13_log_batch_records(self):
        input_data = {
            "fields": [
                "GENDER",
                "AGE",
                "MARITAL_STATUS",
                "PROFESSION",
                'PRODUCT_LINE'
            ],
            "values": [["M", 27, "Single", "Professional", "Personal Accessories"]]
        }

        output_data = {
            "fields": [
                "prediction",
                "probability"
            ],
            "values": [["camping equipment", 0.7205234335053059]]
        }

        records_list = []

        for i in range(0, 10):
            value = randint(0, 20)
            records_list.append(PayloadRecord(request=input_data, response=output_data, response_time=value))

        TestAIOpenScaleClient.subscription.payload_logging.store(records=records_list)

        import time
        time.sleep(120)

    def test_14_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)

    def test_15_stats_on_performance_monitoring_table(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())

        TestAIOpenScaleClient.subscription.performance_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.performance_monitoring.show_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.performance_monitoring.get_table_content(
            format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_16_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_17_disable_performance_monitoring(self):
        TestAIOpenScaleClient.subscription.performance_monitoring.disable()

    def test_18_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_19_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, subscription_uid=TestAIOpenScaleClient.subscription.uid)

    def test_20_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)
        wait_until_deleted(TestAIOpenScaleClient.ai_client, binding_uid=TestAIOpenScaleClient.subscription.binding_uid)

    def test_21_delete_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.delete()
        wait_until_deleted(TestAIOpenScaleClient.ai_client, data_mart=True)
        delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
