from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

# Definir el esquema para los datos del tráfico
schema = StructType() \
    .add("incident", StringType()) \
    .add("location", StringType()) \
    .add("severity", StringType()) \
    .add("timestamp", DoubleType())

# Crear la sesión de Spark
spark = SparkSession.builder \
    .appName("TrafficStreamingApp") \
    .getOrCreate()

# Leer datos de Kafka
traffic_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "traffic_reports") \
    .load()

# Transformar los datos de tráfico
traffic_data = traffic_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Mostrar datos procesados en la consola (solo para pruebas)
query = traffic_data.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Esperar la terminación de la consulta
query.awaitTermination()
