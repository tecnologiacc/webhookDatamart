from os import environ
from flask import Flask, jsonify, request, Response

import json
import os
import pyodbc
import requests

server = '3.129.161.218'
database = 'BD_Datamart'
username = 'Ascenda'
password = 'AscendaP.'
driver = '{ODBC Driver 17 for SQL Server}'

# Conectarse con la DB
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

app = Flask(__name__)

@app.route('/download/<type>/<id>', methods = ['POST'])
def download_document(type, id):
    mensaje = ''
    if request.method == 'POST':
        # Verificar si esta suscrito en la API Datamart
        URL = f'https://api.datamart.pe/subscriptions/v1/check-subscription/20601610664/{id}/RTTSync?check-cred-status=true'
        header = {
            'x-api-key': 'GQeqgT2mcc9W6ee7J1yPV3xApGBI6Cno2xwLtEri',
        }
        r = requests.get(URL, headers=header)

        # Confirmar `subscripcion activa` campo `EstadoCredencial`
        datamart_response = r.json()
        estado_credencial = datamart_response['EstadoCredencial']
        if estado_credencial != 'CredencialValida':
            mensaje = 'Subscripcion inactiva'
            return Response(mensaje, status=400, mimetype='application/json')
        
        # Crear un `cursor` para iterar sobre la DB
        cursor = conn.cursor()

        # Buscar el último documento registrado en la DB
        query = f"""
            SELECT TOP 1 PERCENT
                *
            FROM {database}.dbo.Resp_Webhook
        """

        # Filtrar por `tipo` de documento
        if type == 'RUC':
            query += f"""
                WHERE Respuesta LIKE '%"RUC": "{id}%' 
                ORDER BY FechaRegistro DESC
            """
        elif type == 'RTT':
            query += f"""
                WHERE Respuesta LIKE '%"SubscriberId": "{id}%'
                AND DATEDIFF(day, FechaRegistro, GETDATE()) <= 45
                ORDER BY FechaRegistro DESC
            """
        else:
            mensaje = 'Tipo de documento no permitido'
            return Response(mensaje, status=400)

        # Ejecutar la query
        cursor.execute(query)

        # Obtener los resultados
        result = cursor.fetchall()
        cursor.close()

        # Verificar si hay resultados
        if len(result) == 0:
            mensaje = 'Documento no encontrado'
            return Response(mensaje, status=400, mimetype='application/json')

        # Transformar el string a JSON
        respuesta = json.loads(result[0][1])

        # Usar EnlacePDF
        URL = respuesta['EnlacePdf']
        # Descargar el documento PDF
        r = requests.get(URL, allow_redirects=True)

        # Generar el `path` para el documento con el formato: fecha_id_RTT.pdf
        formato_fecha = result[0][0].strftime('%Y%m%d%H%M%S%f')[:-4]
        ruta = 'C:/websites/webhookpdfdemo'
        file = ''
        if type == 'RUC':
            file = f'{formato_fecha}_{id}_FRUC.pdf'
        elif type == 'RTT':
            file = f'{formato_fecha}_{id}_RTT.pdf'

        if r.status_code == 200:
            with open(os.path.join(ruta, file), 'wb') as f:
                f.write(r.content)
        else:
            mensaje = 'Documento no disponible para descarga'
            return Response(mensaje, status=r.status_code)

        # Verificar si el documento esta descargado
        # en la carpeta `downloads`
        if os.path.isfile(os.path.join(ruta, file)):
            mensaje = 'Documento descargado'
        else:
            mensaje = 'Documento no descargado'

        return Response(mensaje, status=200)

    return Response(mensaje, status=400, mimetype='application/json')

if __name__ == '__main__':
    app.run()
