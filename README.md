# Tarea Sistemas Distribuidos

## Descripción
Este proyecto implementa un sistema de monitoreo de tráfico en tiempo real que obtiene datos de Waze, los envía a Kafka, los procesa con Spark y los almacena en Cassandra para análisis histórico.

## Estructura
- `scrapper/`: Contiene el script para el scraping.
- `kafka/`: Contiene el productor de Kafka y la configuración de Docker Compose.
- `spark_processor/`: Contiene el procesador de Spark Streaming.
- `cassandra/`: Contiene el script de almacenamiento en Cassandra.

## Requisitos
- Python 3
- Docker y Docker Compose
- Apache Spark y PySpark
- Cassandra

## Ejecución
1. Ejecutar `docker-compose.yml` en la carpeta `kafka`:
    ```bash
    docker-compose up -d
    ```

2. Ejecutar el Scrapper:
    ```bash
    python scrapper/scrapper.py
    ```

3. Enviar los datos a Kafka:
    ```bash
    python kafka/producer.py
    ```

4. Procesar los datos en Spark:
    ```bash
    spark-submit spark_processor/spark_processor.py
    ```

5. Almacenar los datos en Cassandra:
    ```bash
    python cassandra/cassandra_storage.py
    ```
