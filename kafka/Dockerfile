# Base image for Spark
FROM bitnami/spark:latest

# Instalar herramientas necesarias
USER root
RUN apt-get update && apt-get install -y netcat-openbsd

# Añadir los conectores de Spark para Kafka
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.3/spark-sql-kafka-0-10_2.12-3.5.3.jar /opt/bitnami/spark/jars/

# Verificar que el jar fue copiado correctamente
RUN test -f /opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.5.3.jar || echo "Error: Kafka connector jar not found!"

# Configurar variables de entorno
ENV SPARK_HOME=/opt/bitnami/spark
WORKDIR $SPARK_HOME

# Cambiar al usuario no-root para mayor seguridad
USER 1001
