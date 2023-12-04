from os import environ
from dotenv import load_dotenv
from flask import Flask, request, Response

import json
import os
import pyodbc
import requests

# Load .env variables
load_dotenv()

server = environ.get('SERVER')
database = environ.get('DATABASE')
username = environ.get('USER')
password = environ.get('PASSWORD')
driver = environ.get('DRIVER')

# Conectarse con la DB
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

app = Flask(__name__)

@app.route('/download/<type>/<id>', methods = ['GET'])
def download_document(type, id):
    json_response = {
        'code': '',
        'message': '',
        'ruta': ''
    }
    if request.method == 'GET':
        # Verificar si esta suscrito en la API Datamart
        URL = f'https://api.datamart.pe/subscriptions/v1/check-subscription/20601610664/{id}/RTTSync?check-cred-status=true'
        header = {
            'x-api-key': 'GQeqgT2mcc9W6ee7J1yPV3xApGBI6Cno2xwLtEri',
        }
        r = requests.get(URL, headers=header)

        # Verificar si se obtuvo una respuesta
        if r.status_code != 200:
            json_response['code'] = '300'
            json_response['message'] = 'Error al consultar la API'
            return Response(
                json.dumps(json_response),
                status=400,
                mimetype='application/json'
            )

        # Confirmar `subscripcion activa` campo `EstadoCredencial`
        datamart_response = r.json()
        estado_credencial = datamart_response['EstadoCredencial']
        if estado_credencial != 'CredencialValida':
            json_response['code'] = '301'
            json_response['message'] = 'Subscripcion inactiva'
            return Response(
                json.dumps(json_response),
                status=400,
                mimetype='application/json'
            )
        
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
            json_response['code'] = '302'
            json_response['message'] = 'Tipo de documento no permitido'
            return Response(
                json.dumps(json_response),
                status=400,
                mimetype='application/json'
            )

        # Ejecutar la query
        cursor.execute(query)

        # Obtener los resultados
        result = cursor.fetchall()
        cursor.close()

        # Verificar si hay resultados
        if len(result) == 0:
            json_response['code'] = '303'
            json_response['message'] = 'Documento no encontrado'
            return Response(
                json.dumps(json_response),
                status=400,
                mimetype='application/json'
            )

        # Transformar el string a JSON
        respuesta = json.loads(result[0][1])

        # Usar EnlacePDF
        URL = respuesta['EnlacePdf']
        # Descargar el documento PDF
        r = requests.get(URL, allow_redirects=True)

        # Generar el `path` para el documento con el formato: fecha_id_RTT.pdf
        formato_fecha = result[0][0].strftime('%Y%m%d%H%M%S%f')[:-4]
        ruta = os.path.join(os.path.expanduser('~'), 'Downloads')
        # ruta = 'C:/websites/webhookpdfdemo'
        file = ''
        if type == 'RUC':
            file = f'{formato_fecha}_{id}_FRUC.pdf'
        elif type == 'RTT':
            file = f'{formato_fecha}_{id}_RTT.pdf'

        if r.status_code == 200:
            with open(os.path.join(ruta, file), 'wb') as f:
                f.write(r.content)
        else:
            json_response['code'] = '304'
            json_response['message'] = 'Documento no disponible para descarga'
            return Response(
                json.dumps(json_response),
                status=400,
                mimetype='application/json'
            )

        # Verificar si el documento esta descargado
        # en la carpeta `downloads`
        if os.path.isfile(os.path.join(ruta, file)):
            json_response['code'] = '200'
            json_response['message'] = 'Documento descargado'
        else:
            json_response['code'] = '305'
            json_response['message'] = 'Documento no descargado'
        json_response['ruta'] = os.path.join(ruta, file)

        return Response(
            json.dumps(json_response),
            status=200,
            mimetype='application/json'
        )

    return Response(json_response, status=400, mimetype='application/json')

if __name__ == '__main__':
    app.run()
