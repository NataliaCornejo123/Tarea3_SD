# kafka/producer.py

from confluent_kafka import Producer
import json

# Configuración del productor de Confluent Kafka
producer_config = {
    'bootstrap.servers': 'localhost:9092',  # Dirección del servidor de Kafka
}

producer = Producer(producer_config)

def enviar_dato_a_kafka(data):
    # Callback para manejar la confirmación de entrega de Kafka
    def acked(err, msg):
        if err is not None:
            print(f"Error al enviar mensaje: {err}")
        else:
            print(f"Mensaje enviado: {msg.value().decode('utf-8')}")

    # Enviar cada dato de incidente a Kafka
    for incidente in data:
        producer.produce('waze_topic', value=json.dumps(incidente), callback=acked)
        producer.poll(0)  # Llama a poll para manejar los eventos de envío

    # Esperar a que todos los mensajes se envíen
    producer.flush()

if __name__ == "__main__":
    # Leer los datos de incidentes desde el archivo JSON
    with open("../scrapper/incidentes.json", "r") as file:
        incidentes = json.load(file)
    
    # Enviar datos a Kafka
    enviar_dato_a_kafka(incidentes)
