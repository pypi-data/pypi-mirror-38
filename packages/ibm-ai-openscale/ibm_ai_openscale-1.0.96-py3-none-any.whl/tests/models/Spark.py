from .AbstractModel import AbstractModel

import os
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, DoubleType, StringType, ArrayType
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, IndexToString, VectorAssembler, RFormula
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.regression import LinearRegression


class GoSales(AbstractModel):

    file_path = "datasets/GoSales/GoSales_Tx_NaiveBayes.csv"

    def __init__(self):
        spark = SparkSession.builder.getOrCreate()

        df_data = spark.read \
            .format('org.apache.spark.sql.execution.datasources.csv.CSVFileFormat') \
            .option('header', 'true') \
            .option('inferSchema', 'true') \
            .load(self.file_path)

        splitted_data = df_data.randomSplit([0.8, 0.18, 0.02], 24)
        train_data = splitted_data[0]
        test_data = splitted_data[1]
        predict_data = splitted_data[2]

        stringIndexer_label = StringIndexer(inputCol="PRODUCT_LINE", outputCol="label").fit(df_data)
        stringIndexer_prof = StringIndexer(inputCol="PROFESSION", outputCol="PROFESSION_IX")
        stringIndexer_gend = StringIndexer(inputCol="GENDER", outputCol="GENDER_IX")
        stringIndexer_mar = StringIndexer(inputCol="MARITAL_STATUS", outputCol="MARITAL_STATUS_IX")

        vectorAssembler_features = VectorAssembler(inputCols=["GENDER_IX", "AGE", "MARITAL_STATUS_IX", "PROFESSION_IX"],
                                                   outputCol="features")
        rf = RandomForestClassifier(labelCol="label", featuresCol="features")
        labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                                       labels=stringIndexer_label.labels)
        pipeline_rf = Pipeline(stages=[stringIndexer_label, stringIndexer_prof, stringIndexer_gend, stringIndexer_mar,
                                       vectorAssembler_features, rf, labelConverter])
        model_rf = pipeline_rf.fit(train_data)

        self.model = model_rf
        self.pipeline = pipeline_rf
        self.training_data = train_data
        self.test_data = test_data
        self.prediction = predict_data
        self.labels = stringIndexer_label.labels

    def publish_to_wml(self, wml_client):
        return wml_client.repository.store_model(model=self.model, meta_props=self.get_model_props(wml_client), training_data=self.training_data, pipeline=self.pipeline)

    def get_model_props(self, wml_client):
        return {
            wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
            wml_client.repository.ModelMetaNames.NAME: self.get_name()
        }

    def get_name(self):
        return "spark_gosales_model"

    def get_scoring_payload(self):
        return {
           "fields": [
              "GENDER",
              "AGE",
              "MARITAL_STATUS",
              "PROFESSION"
           ],
           "values": [
              [
                 "M",
                 23,
                 "Single",
                 "Student"
              ],
              [
                 "M",
                 55,
                 "Single",
                 "Executive"
              ]
           ]
        }


class Telco(AbstractModel):
    file_path = os.path.join(os.getcwd(), 'datasets', 'SparkMlibRegression', 'WA_FnUseC_TelcoCustomerChurn.csv')

    def __init__(self):

        spark = SparkSession.builder.getOrCreate()

        df_data = spark.read \
            .format('org.apache.spark.sql.execution.datasources.csv.CSVFileFormat') \
            .option('header', 'true') \
            .option('inferSchema', 'true') \
            .option('nanValue', ' ') \
            .option('nullValue', ' ') \
            .load(self.file_path)

        df_complete = df_data.dropna()
        df_complete.drop('Churn')

        (train_data, test_data) = df_complete.randomSplit([0.8, 0.2], 24)

        features = RFormula(
            formula="~ gender + SeniorCitizen +  Partner + Dependents + tenure + PhoneService + MultipleLines + "
                    "InternetService + OnlineSecurity + OnlineBackup + DeviceProtection + TechSupport + StreamingTV + "
                    "StreamingMovies + Contract + PaperlessBilling + PaymentMethod + MonthlyCharges - 1")

        lr = LinearRegression(labelCol='TotalCharges')
        pipeline_lr = Pipeline(stages=[features, lr])
        lr_model = pipeline_lr.fit(train_data)
        lr_predictions = lr_model.transform(test_data)

        self.model = lr_model
        self.pipeline = pipeline_lr
        self.training_data = train_data
        self.test_data = test_data
        self.prediction = lr_predictions

    def publish_to_wml(self, wml_client):
        return wml_client.repository.store_model(model=self.model, meta_props=self.get_model_props(wml_client), training_data=self.training_data, pipeline=self.pipeline)

    def get_model_props(self, wml_client):
        return {
            wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
            wml_client.repository.ModelMetaNames.NAME: "Telco Spark Model"
        }

    def get_scoring_payload(self):
        return {
            "fields": [
                "customerID",
                "gender",
                "SeniorCitizen",
                "Partner",
                "Dependents",
                "tenure",
                "PhoneService",
                "MultipleLines",
                "InternetService",
                "OnlineSecurity",
                "OnlineBackup",
                "DeviceProtection",
                "TechSupport",
                "StreamingTV",
                "StreamingMovies",
                "Contract",
                "PaperlessBilling",
                "PaymentMethod",
                "MonthlyCharges"
            ],
            "values": [
                [
                    "9237-HQITU",
                    "Female",
                    0,
                    "No",
                    "No",
                    20,
                    "Yes",
                    "No",
                    "Fiber optic",
                    "No",
                    "No",
                    "No",
                    "No",
                    "No",
                    "No",
                    "Month-to-month",
                    "Yes",
                    "Electronic check",
                    70.7
                ],
                [
                    "3638-WEABW",
                    "Female",
                    0,
                    "Yes",
                    "No",
                    58,
                    "Yes",
                    "Yes",
                    "DSL",
                    "No",
                    "Yes",
                    "No",
                    "Yes",
                    "No",
                    "No",
                    "Two year",
                    "Yes",
                    "Credit card (automatic)",
                    59.900
                ],
                [
                    "8665-UTDHZ",
                    "Male",
                    0,
                    "Yes",
                    "Yes",
                    1,
                    "No",
                    "No phone service",
                    "DSL",
                    "No",
                    "Yes",
                    "No",
                    "No",
                    "No",
                    "No",
                    "Month-to-month",
                    "No",
                    "Electronic check",
                    30.200
                ],
                [
                    "8773-HHUOZ",
                    "Female",
                    0,
                    "No",
                    "Yes",
                    17,
                    "Yes",
                    "No",
                    "DSL",
                    "No",
                    "No",
                    "No",
                    "No",
                    "Yes",
                    "Yes",
                    "Month-to-month",
                    "Yes",
                    "Mailed check",
                    64.700
                ]
            ]
        }


class BestHeartDrug(AbstractModel):

    training_data_path = "datasets/BestHeartDrug/drug_train_data.csv"
    feedback_data_path = "datasets/drugs/drug_feedback_test.csv"

    def __init__(self):
        spark = SparkSession.builder.getOrCreate()

        df_data = spark.read \
            .format('org.apache.spark.sql.execution.datasources.csv.CSVFileFormat') \
            .option('header', 'true') \
            .option("delimiter", ';') \
            .option('inferSchema', 'true') \
            .load(self.training_data_path)

        df_test = spark.read \
            .format('org.apache.spark.sql.execution.datasources.csv.CSVFileFormat') \
            .option('header', 'true') \
            .option("delimiter", ';') \
            .option('inferSchema', 'true') \
            .load(self.feedback_data_path)

        stringIndexer_label = StringIndexer(inputCol="DRUG", outputCol="label").fit(df_data)
        stringIndexer_sex = StringIndexer(inputCol="SEX", outputCol="SEX_IX")
        stringIndexer_bp = StringIndexer(inputCol="BP", outputCol="BP_IX")
        stringIndexer_chol = StringIndexer(inputCol="CHOLESTEROL", outputCol="CHOLESTEROL_IX")

        vectorAssembler_features = VectorAssembler(inputCols=["AGE", "SEX_IX", "BP_IX", "CHOLESTEROL_IX", "NA", "K"],
                                                   outputCol="features")
        rf = RandomForestClassifier(labelCol="label", featuresCol="features")
        labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                                       labels=stringIndexer_label.labels)
        pipeline_rf = Pipeline(stages=[stringIndexer_label, stringIndexer_sex, stringIndexer_bp, stringIndexer_chol,
                                       vectorAssembler_features, rf, labelConverter])
        model_rf = pipeline_rf.fit(df_data)

        train_data_schema = df_data.schema
        label_field = next(f for f in train_data_schema.fields if f.name == "DRUG")
        label_field.metadata['values'] = stringIndexer_label.labels

        input_fileds = filter(lambda f: f.name != "DRUG", train_data_schema.fields)

        output_data_schema = StructType(list(input_fileds)). \
            add("prediction", DoubleType(), True, {'modeling_role': 'prediction'}). \
            add("predictedLabel", StringType(), True,
                {'modeling_role': 'decoded-target', 'values': stringIndexer_label.labels}). \
            add("probability", ArrayType(DoubleType()), True, {'modeling_role': 'probability'})

        self.model = model_rf
        self.pipeline = pipeline_rf
        self.training_data = df_data
        self.test_data = df_test
        self.output_data_schema = output_data_schema

    def publish_to_wml(self, wml_client):
        pass

    def get_model_props(self, wml_client):
        pass

    def get_scoring_payload(self):
        return {
            "fields": [
                "AGE",
                "SEX",
                "BP",
                "CHOLESTEROL",
                "NA",
                "K"
            ],
            "values": [
                [
                    20.0,
                    "F",
                    "HIGH",
                    "HIGH",
                    0.71,
                    0.07
                ],
                [
                    55.0,
                    "M",
                    "LOW",
                    "HIGH",
                    0.71,
                    0.07
                ]
            ]
        }

    def get_scoring_payload_from_training_data(self):
        test_data = pd.read_csv(self.training_data_path, header=0, sep=';')
        sample = test_data.sample()

        return {
            "fields": [
                "AGE",
                "SEX",
                "BP",
                "CHOLESTEROL",
                "NA",
                "K"
            ],
            "values": [
                [
                    sample.iloc[0]['AGE'],
                    sample.iloc[0]['SEX'],
                    sample.iloc[0]['BP'],
                    sample.iloc[0]['CHOLESTEROL'],
                    sample.iloc[0]['NA'],
                    sample.iloc[0]['K']
                ]
            ]
        }