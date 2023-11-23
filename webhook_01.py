from os import environ
from dotenv import load_dotenv
from flask import Flask, jsonify

import pyodbc
from requests import request

# Load .env variables
load_dotenv()

server = environ.get('SERVER')
database = environ.get('DATABASE')
username = environ.get('USER')
password = environ.get('PASSWORD')
driver = environ.get('DRIVER')

# Conectarse con la DB
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=Yes')

app = Flask(__name__)

def insertar_data_tabla(tabla, data, cursor):
    for row in data:
        # Crear `query` de inserción
        columns = ', '.join(row.keys())
        placeholders = ', '.join('?' * len(row))
        query = f"INSERT INTO {tabla} ({columns}) VALUES ({placeholders})"
        
        # Ejecutar la query
        cursor.execute(query, list(row.values()))

@app.route('/webhook', methods = ['POST'])
def get_notification():
    # Crear un `cursor` para iterar sobre la DB
    cursor = conn.cursor()

    data = request.json
    RUC = data.get('RUC')
    RTT = data.get('RTRIB')

    if RUC:
        # Procesar RUC
        mensaje = {}
    elif RTT:
        # Procesar RTT
        mensaje = {}
    else:
        cursor.close()

    return jsonify({'mensaje': 'Notificacion recibida'})

if __name__ == '__main__':
    app.run()
