# spark_processor/spark_processor.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType

# Configuración de Spark
spark = SparkSession.builder \
    .appName("WazeProcessor") \
    .getOrCreate()

# Configuración de Kafka como fuente de datos en Spark
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "waze_topic") \
    .load()

# Definición del esquema de los datos
schema = StructType().add("tipo", StringType()).add("ubicacion", StringType()).add("hora", StringType())
incidents = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data")).select("data.*")

# Procesamiento de los datos (Ejemplo)
incidents.writeStream \
    .format("console") \
    .start() \
    .awaitTermination()
