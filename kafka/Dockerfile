# Utilizar una imagen base con las herramientas necesarias ya instaladas
FROM openjdk:8-jdk  

# Descargar e instalar Spark manualmente
RUN apt-get update && \
    apt-get install -y curl python3-pip netcat-openbsd && \
    curl -L -o /tmp/spark.tgz https://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz && \
    tar -xzf /tmp/spark.tgz -C /opt && \
    mv /opt/spark-3.1.1-bin-hadoop3.2 /opt/spark && \
    rm /tmp/spark.tgz && \
    pip3 install elasticsearch && \
    rm -rf /var/lib/apt/lists/*

# Añadir los conectores de Spark para Kafka
ADD https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.1.1/spark-sql-kafka-0-10_2.12-3.1.1.jar /opt/spark/jars/

# Añadir el conector de ElasticSearch para Spark
ADD https://repo1.maven.org/maven2/org/elasticsearch/elasticsearch-spark-30_2.12/8.3.3/elasticsearch-spark-30_2.12-8.3.3.jar /opt/spark/jars/

# Crear un directorio para configuraciones
RUN mkdir -p /opt/spark/conf

# Copiar el archivo de configuración spark-defaults.conf
COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf

# Configurar variables de entorno
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Cambiar permisos para el usuario no-root
RUN chown -R 1001:1001 /opt/spark

# Cambiar al usuario no-root para mayor seguridad
USER 1001

# Cambiar al directorio de trabajo de Spark
WORKDIR $SPARK_HOME
