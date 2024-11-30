# Base image for Spark
FROM bitnami/spark:latest

# Add Spark-Kafka connectors
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.3/spark-sql-kafka-0-10_2.12-3.5.3.jar /opt/bitnami/spark/jars/

# Set environment variables
ENV SPARK_HOME=/opt/bitnami/spark
WORKDIR $SPARK_HOME
