
from elasticsearch import Elasticsearch
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

# Crear la sesión de Spark
spark = SparkSession.builder \
    .appName("TrafficStreamingApp") \
    .config("spark.jars", "./spark-jars/spark-sql-kafka-0-10_2.12-3.3.0.jar,./spark-jars/kafka-clients-3.3.0.jar,./spark-jars/commons-pool2-2.11.1.jar,./spark-jars/jackson-core-2.12.3.jar,./spark-jars/jackson-databind-2.12.3.jar,./spark-jars/jackson-annotations-2.12.3.jar,./spark-jars/spark-token-provider-kafka-0-10_2.12-3.3.0.jar") \
    .config("spark.hadoop.io.nativeio.use", "false") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
    .getOrCreate()

# Configuración de logs de Spark para reducir la salida excesiva en consola
spark.sparkContext.setLogLevel("WARN")

# Configuración de Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

# Definir el esquema para los datos del tráfico
schema = StructType() \
    .add("incident", StringType()) \
    .add("location", StringType()) \
    .add("severity", StringType()) \
    .add("timestamp", DoubleType())

# Leer datos de Kafka
kafka_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "traffic_reports") \
    .load()

# Transformar los datos de tráfico
traffic_data = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Función para escribir cada micro-batch a Elasticsearch
def write_to_elasticsearch(batch_df, batch_id):
    # Convertir el DataFrame a Pandas para interactuar con Elasticsearch
    batch_pandas = batch_df.toPandas()
    for _, row in batch_pandas.iterrows():
        doc = {
            "incident": row["incident"],
            "location": row["location"],
            "severity": row["severity"],
            "timestamp": row["timestamp"]
        }
        es.index(index="traffic_incidents", body=doc)

# Aplicar la escritura de los datos a Elasticsearch usando foreachBatch
query = traffic_data.writeStream \
    .foreachBatch(write_to_elasticsearch) \
    .outputMode("append") \
    .start()

# Esperar la terminación de la consulta
query.awaitTermination()
