import pandas as pd
from delta import *
from pyspark.sql import SparkSession
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_spark_session():
    return (SparkSession.builder
            .appName("CervejariasETL")
            .config("spark.jars.packages", "io.delta:delta-core:0.8.0")
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            .getOrCreate())

def load_bronze(**kwargs):
    try:
        spark = get_spark_session()
        df = spark.read.parquet('/tmp/raw_data.parquet')
        df.write.format("delta").mode("overwrite").save("/delta/cervejarias_bronze")
        logger.info("Dados carregados na camada Bronze com sucesso")
    except Exception as e:
        logger.error(f"Erro ao carregar dados na camada Bronze: {str(e)}")
        raise

def load_silver(**kwargs):
    try:
        spark = get_spark_session()
        df = spark.read.parquet('/tmp/silver_data.parquet')
        df.write.format("delta").partitionBy("pais").mode("overwrite").save("/delta/cervejarias_silver")
        logger.info("Dados carregados na camada Silver com sucesso")
    except Exception as e:
        logger.error(f"Erro ao carregar dados na camada Silver: {str(e)}")
        raise

def load_gold(**kwargs):
    try:
        spark = get_spark_session()
        df = spark.read.parquet('/tmp/gold_data.parquet')
        df.write.format("delta").mode("overwrite").save("/delta/cervejarias_gold")
        logger.info("Dados carregados na camada Gold com sucesso")
    except Exception as e:
        logger.error(f"Erro ao carregar dados na camada Gold: {str(e)}")
        raise

if __name__ == "__main__":
    load_bronze()
    load_silver()
    load_gold()