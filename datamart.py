from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, Response
from os import environ

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
ruta = environ.get('RUTA')

app = Flask(__name__)

def verify_datamart_subscription(id):
    """ Verificar si el usuario esta suscrito en la API Datamart
    
    Parameters
    ----------
    id : str
        Clave SOL del cliente
    Returns
    -------
    response : requests.models.Response
        Respuesta de la API Datamart

    """
    URL = f'https://api.datamart.pe/subscriptions/v1/check-subscription/20601610664/{id}/RTTSync?check-cred-status=true'
    header = {
        'x-api-key': 'GQeqgT2mcc9W6ee7J1yPV3xApGBI6Cno2xwLtEri',
    }

    return requests.get(URL, headers = header)

@app.route('/download/RUC/<id>', methods = ['GET'])
def download_ruc_document(id):
    """ Descargar el documento PDF del RUC

    Parameters
    ----------
    id : str
        Número de RUC del cliente
    Returns
    -------
    response : flask.wrappers.Response
        Respuesta del endpoint
    """
    try:
        json_response = {
            'code': '',
            'message': '',
            'ruta': ''
        }

        # Verificar si esta suscrito en la API Datamart
        r = verify_datamart_subscription(id)
        if r.status_code != 200:
            json_response['code'] = '300'
            json_response['message'] = 'Error al consultar la API de Datamart'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        # Confirmar `subscripcion activa` campo `EstadoCredencial`
        datamart_json = r.json()
        estado_credencial = datamart_json['EstadoCredencial']
        if estado_credencial != 'CredencialValida':
            json_response['code'] = '301'
            json_response['message'] = 'Subscripcion inactiva'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        # Crear la conexión a la DB
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )

        # Crear un `cursor` para iterar sobre la DB
        cursor = conn.cursor()

        # Buscar el último documento registrado en la DB
        query = f"""
            SELECT TOP 1 PERCENT
                *
            FROM {database}.dbo.Resp_Webhook
            WHERE Respuesta LIKE '%"RUC": "{id}%' 
            ORDER BY FechaRegistro DESC
        """

        # Ejecutar la query y obtener los resultados
        result = cursor.execute(query).fetchall()
        cursor.close()

        # Verificar si hay resultados
        if len(result) == 0:
            json_response['code'] = '303'
            json_response['message'] = 'Documento no encontrado'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        # Transformar el string a JSON
        respuesta = json.loads(result[0][1])

        # Usar EnlacePDF
        URL = respuesta['EnlacePdf']
        # Descargar el documento PDF
        r = requests.get(URL, allow_redirects = True)

        # Generar el `path` para el documento con el formato: fecha_id_RUC.pdf
        formato_fecha = result[0][0].strftime('%Y%m%d%H%M%S%f')[:-4]
        file = f'{formato_fecha}_{id}_FRUC.pdf'

        # Verificar estado de la descarga
        if r.status_code == 200:
            # Guardar el documento en la ruta especificada
            with open(os.path.join(ruta, file), 'wb') as f:
                f.write(r.content)
        else:
            json_response['code'] = '304'
            json_response['message'] = 'Documento no disponible para descarga'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        # Verificar si el documento se ha guardado
        if os.path.isfile(os.path.join(ruta, file)):
            json_response['code'] = '200'
            json_response['message'] = 'Documento descargado'
        else:
            json_response['code'] = '305'
            json_response['message'] = 'Documento no descargado'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        json_response['ruta'] = 'Files/Persons/' + file

        return Response(
            json.dumps(json_response),
            status = 200,
            mimetype = 'application/json'
        )
    except Exception as e:
        json_response['error'] = str(e)
        return Response(
            json.dumps(json_response),
            status = 500,
            mimetype = 'application/json'
        )

@app.route('/download/RTT/<id>', methods = ['GET'])
def download_rtt_document(id):
    """ Descargar el documento PDF del RTT

    Parameters
    ----------
    id : str
        Número de RUC del cliente
    Returns
    -------
    response : flask.wrappers.Response
        Respuesta del endpoint
    """
    try:
        json_response = {
            'code': '',
            'message': '',
            'ruta': ''
        }

        # Verificar si esta suscrito en la API Datamart
        r = verify_datamart_subscription(id)
        if r.status_code != 200:
            json_response['code'] = '300'
            json_response['message'] = 'Error al consultar la API de Datamart'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        # Confirmar `subscripcion activa` campo `EstadoCredencial`
        datamart_json = r.json()
        estado_credencial = datamart_json['EstadoCredencial']
        if estado_credencial != 'CredencialValida':
            json_response['code'] = '301'
            json_response['message'] = 'Subscripcion inactiva'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        # Crear la conexión a la DB
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )

        # Crear un `cursor` para iterar sobre la DB
        cursor = conn.cursor()

        # Buscar el último documento registrado en la DB
        query = f"""
            SELECT TOP 1 PERCENT
                *
            FROM {database}.dbo.Resp_Webhook
            WHERE Respuesta LIKE '%"SubscriberId": "{id}%' 
            ORDER BY FechaRegistro DESC
        """

        # Ejecutar la query y obtener los resultados
        result = cursor.execute(query).fetchall()
        cursor.close()

        # Verificar si hay resultados
        if len(result) == 0:
            json_response['code'] = '303'
            json_response['message'] = 'Documento no encontrado'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        # Verificar vigencia de la subscripcion < 45 dias
        fecha_registro = result[0][0]
        fecha_actual = datetime.now()
        dias = (fecha_actual - fecha_registro).days
        if dias > 45:
            json_response['code'] = '306'
            json_response['message'] = 'Documento fuera de vigencia'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        # Transformar el string a JSON
        respuesta = json.loads(result[0][1])

        # Usar EnlacePDF
        URL = respuesta['EnlacePdf']
        # Descargar el documento PDF
        r = requests.get(URL, allow_redirects = True)

        # Generar el `path` para el documento con el formato: fecha_id_RUC.pdf
        formato_fecha = result[0][0].strftime('%Y%m%d%H%M%S%f')[:-4]
        file = f'{formato_fecha}_{id}_FRTT.pdf'

        # Verificar estado de la descarga
        if r.status_code == 200:
            # Guardar el documento en la ruta especificada
            with open(os.path.join(ruta, file), 'wb') as f:
                f.write(r.content)
        else:
            json_response['code'] = '304'
            json_response['message'] = 'Documento no disponible para descarga'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        # Verificar si el documento se ha guardado
        if os.path.isfile(os.path.join(ruta, file)):
            json_response['code'] = '200'
            json_response['message'] = 'Documento descargado'
        else:
            json_response['code'] = '305'
            json_response['message'] = 'Documento no descargado'
            return Response(
                json.dumps(json_response),
                status = 400,
                mimetype = 'application/json'
            )

        json_response['ruta'] = 'Files/Persons' + file

        return Response(
            json.dumps(json_response),
            status = 200,
            mimetype = 'application/json'
        )
    except Exception as e:
        json_response['error'] = str(e)
        return Response(
            json.dumps(json_response),
            status = 500,
            mimetype = 'application/json'
        )

if __name__ == '__main__':
    app.run()