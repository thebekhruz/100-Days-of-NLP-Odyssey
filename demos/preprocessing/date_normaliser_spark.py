import sparknlp
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField
from pyspark.sql.functions import explode, concat_ws, lit, col


from sparknlp.base import DocumentAssembler
from sparknlp.base import Pipeline
from sparknlp.annotator import DateMatcher

import pandas as pd


def initialize_spark(app_name="Spark NLP DateMatcher Example"):
    """ Initialize and return a Spark session with Spark NLP."""
    return SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:3.4.0") \
        .getOrCreate()


def create_nlp_pipeline():
    """ Create and return a Spark NLP pipeline with DocumentAssembler and DateMatcher."""
    document_assembler = DocumentAssembler() \
        .setInputCol("text") \
        .setOutputCol("document")

    date_matcher = DateMatcher() \
        .setInputCols(["document"]) \
        .setOutputCol("date") \
        .setOutputFormat("yyyy-MM-dd")

    return Pipeline(stages=[document_assembler, date_matcher])


def process_dates_with_spark_nlp(spark_df):
    """ Process dates in a Spark DataFrame and return original text alongside the detected sentence. """
    document_assembler = DocumentAssembler() \
        .setInputCol("text") \
        .setOutputCol("document")

    date_matcher = DateMatcher() \
        .setInputCols(["document"]) \
        .setOutputCol("date") \
        .setOutputFormat("yyyy-MM-dd")

    pipeline = Pipeline(stages=[document_assembler, date_matcher])
    result = pipeline.fit(spark_df).transform(spark_df)


    result = result.withColumn("date", explode("date.result")) \
                   .withColumn("sentence", concat_ws(" ", "date")) \
                   .select("doc_id", col("text").alias("original_text"), "sentence")

    return result


def save_processed_data(doc_ids, processed_texts, output_file_path, types):
    """Save processed texts with their doc_ids to a CSV file."""
    processed_df = pd.DataFrame({'doc_id': doc_ids, 'type': types, 'value': processed_texts})
    processed_df.to_csv(output_file_path, sep='\t', index=False, header=None)


def get_texts_with_ids(df, text_type):
    """Get texts and their doc_ids based on type (title/description)."""
    relevant_df = df[df['type'] == text_type]
    return relevant_df['doc_id'].tolist(), relevant_df['value'].tolist()


def main():
    spark = initialize_spark()
    
    input_file_path = 'data/raw_data/partitions/partition_2500ent.csv'
    df = pd.read_csv(input_file_path, delimiter='\t', header=None, names=['doc_id', 'type', 'value'])
    
    doc_ids, titles = get_texts_with_ids(df, 'title')
    
    # Prepare titles with doc_ids for Spark processing
    titles_with_ids = list(zip(doc_ids, titles))
    schema = StructType([
        StructField("doc_id", StringType(), True),
        StructField("text", StringType(), True)
    ])
    titles_df = spark.createDataFrame(titles_with_ids, schema=schema)
    
    # Adjust process_dates_with_spark_nlp to accept and return doc_id
    result_df = process_dates_with_spark_nlp( titles_df)
    
    # Now result_df should include doc_ids, ensuring alignment
    processed_results = result_df.toPandas()

    # Save directly since processed_results already includes doc_ids and processed titles
    output_file_path = 'data/processed_data/processed_titles.csv'
    processed_results.to_csv(output_file_path, sep='\t', index=False, header=None)



if __name__ == "__main__":
    main()

