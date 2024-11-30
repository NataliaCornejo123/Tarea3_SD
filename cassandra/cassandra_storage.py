# cassandra/cassandra_storage.py

from cassandra.cluster import Cluster
from uuid import uuid4
import json

# Configuración de Cassandra
cluster = Cluster(['localhost'])
session = cluster.connect()

# Crear Keyspace y Tabla
session.execute("""
CREATE KEYSPACE IF NOT EXISTS waze_data
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
""")
session.set_keyspace('waze_data')
session.execute("""
CREATE TABLE IF NOT EXISTS incidentes (
    id UUID PRIMARY KEY,
    tipo TEXT,
    ubicacion TEXT,
    hora TEXT
);
""")

# Insertar datos
def almacenar_incidente(data):
    session.execute("""
    INSERT INTO incidentes (id, tipo, ubicacion, hora)
    VALUES (%s, %s, %s, %s)
    """, (uuid4(), data['tipo'], data['ubicacion'], data['hora']))

if __name__ == "__main__":
    with open("incidentes.json", "r") as file:
        incidentes = json.load(file)
        for incidente in incidentes:
            almacenar_incidente(incidente)
