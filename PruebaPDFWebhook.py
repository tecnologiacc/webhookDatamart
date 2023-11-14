#!/usr/bin/env python
# coding: utf-8

# In[34]:


from flask import Flask, request, abort, jsonify
import requests
import pyodbc
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, LongTable,Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet



# app=Flask(__name__)

# SQL Server connection details
server = '3.129.161.218'
database = 'BD_Datamart'
username = 'Ascenda'
password = 'AscendaP.'
driver = '{ODBC Driver 17 for SQL Server}' 

conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')


def insertar_en_tabla(tabla, data, cursor):
        
    for element in data: 
        # Crear la query de inserción
        columns = ', '.join(element.keys())
        placeholders = ', '.join('?' * len(element))
        query = f"INSERT INTO {tabla} ({columns}) VALUES ({placeholders})"
        
        # Ejecutar la query
        cursor.execute(query, list(element.values()))
        #conn.commit()
        
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer

def crear_pdf(titulo_general, tablas, titulos, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    titulo_style = styles["Heading3"]
    titulo_style.alignment = 0  # 0 significa alinear a la izquierda
    
    # Añadir título general
    styles = getSampleStyleSheet()
    title = Paragraph("<u>" + titulo_general + "</u>", styles['Heading1'])
    story.append(title)
    story.append(Spacer(1, 24))  # Añadir espacio después del título

    for i, tabla_data in enumerate(tablas):
         # Añadir el título
        titulo = Paragraph("<b>%s</b>" % titulos[i], titulo_style)
        story.append(titulo)
        story.append(Spacer(1, 12))
        
        # Usar LongTable para manejar tablas que pueden abarcar múltiples páginas
        tabla = LongTable(tabla_data, repeatRows=1)  # repeatRows=1 repite el encabezado de la tabla en cada página nueva
        tabla.hAlign = 'LEFT'  # Alinear la tabla a la izquierda
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente normal para el contenido
            ('FONTSIZE', (0, 0), (-1, -1), 6),  # Tamaño de fuente más pequeño para ajustar más contenido
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente en el centro
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('SPLITLATE', (0, 0), (-1, -1), True),  # Evita que las celdas se dividan entre páginas
        ]))

        # Añadir espacio después de cada tabla (si hay múltiples)
        story.append(tabla)
        story.append(Spacer(1, 12))

    doc.build(story)

    
@app.route('/webhook',methods=['POST'])
def webhook():
    if(request.method == 'POST' ):
        cursor = conn.cursor()#Conectar a base de datos

data='{"DatamartReport": {"@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance", "@xmlns:xsd": "http://www.w3.org/2001/XMLSchema", "RTRIB": {"CaracteristicasTributarias": {"CPE": {"FchEmisorElectronico": null, "Sistema": [{"Desde": "09/07/2018", "Text": "FACTURA PORTAL"}, {"Desde": "06/30/2020", "Text": "BOLETA PORTAL"}, {"Desde": "02/10/2023", "Text": "DESDE LOS SISTEMAS DEL CONTRIBUYENTE. AUTORIZ"}], "SistemaEmisionCP": "COMPUTARIZADO"}, "DependenciaSUNAT": {"Cod": null, "Nombre": "INTENDENCIA LIMA"}, "EstadoContribuyenteSUNAT": {"CondicionContribuyente": "HABIDO", "ContribuyenteEstado": "ACTIVO", "ReinicioActividades": null, "SuspencionActividades": null}, "FchInicioActividad": "03/10/2007", "Padrones": null, "RegistroTributosVinculados": null, "SLEPLE": {"FechaInscripcionPle": "01/01/2015", "SistemaContabilidad": "COMPUTARIZADO"}}, "Fecha": "02/10/2023 16:55", "Id": null, "InfoEmpresa": {"Caracteristicas": {"Actecos": [{"Acteco": ["VENTA AL POR MAYOR NO ESPECIALIZADA"], "Glosa": "Actividad Econ\u00f3mica"}, {"Acteco": ["03 IMPORTADOR/EXPORTADOR"], "Glosa": "Actividad de Comercio Exterior"}], "CompPagos": {"CompPago": ["FACTURA", "BOLETA DE VENTA", "LIQUIDACION DE COMPRA", "NOTA DE CREDITO", "GUIA DE REMISION - REMITENTE"], "Glosa": "Comprobantes de Pago Autorizados"}, "Empleados": null, "TipoSociedad": null}, "Identificacion": {"Documento": {"Numero": null, "Tipo": ""}, "NombreComercial": "-", "RazonSocial": "CONSORCIO GLM S.A.C.", "RUC": "20517160432"}, "InformacionAl": "07/01/2023", "Localizacion": {"Contactos": null, "Direcciones": [{"Condicion": null, "Departamento": null, "Distrito": null, "Dpto": null, "Interior": null, "Km": null, "Lote": null, "Mz": null, "Nombre": null, "Numero": null, "OtrasRef": null, "Provincia": null, "Tipo": "DOMICILIO FISCAL", "TipoPropiedad": null, "Ubugeo": null, "Via": null, "Zona": null}]}, "NroActualizacion": null, "ProfesionOficio": null}, "InfoFinanciera": {"DeclaracionesAnuales": {"InfoEcoFin": [{"Anno": 2022, "Campo": [{"Codigo": "Ingresos Netos del periodo", "Text": "14,806,410", "Tipo": "O"}, {"Codigo": "Otros Ingresos declarados", "Text": "45,658", "Tipo": "R"}, {"Codigo": "Total Activos Netos", "Text": "11,438,531", "Tipo": "R"}, {"Codigo": "Cuentas Por Cobrar Comerciales - Terceros", "Text": "1,740,410", "Tipo": "R"}, {"Codigo": "Cuentas Por Cobrar Comerciales - Relacionados", "Text": null, "Tipo": "S"}, {"Codigo": "Cuentas Por Cobrar Diversas - Terceros", "Text": "299,708", "Tipo": "O"}, {"Codigo": "Cuentas Por Cobrar Diversas - Relacionados", "Text": null, "Tipo": "S"}, {"Codigo": "Cuentas por cobrar a accionistas, socios, directores", "Text": null, "Tipo": "S"}, {"Codigo": "Provisi\u00f3n por cuentas de cuentas de cobranza dudosa", "Text": null, "Tipo": "S"}, {"Codigo": "Total Cuentas por Pagar (proveedores / de terceros / a relacionados)", "Text": "3,349,259", "Tipo": "R"}, {"Codigo": "Total Pasivo", "Text": "3,870,991", "Tipo": "R"}, {"Codigo": "Total patrimonio", "Text": "7,567,540", "Tipo": "R"}, {"Codigo": "Capital social", "Text": "2,459,522", "Tipo": "O"}, {"Codigo": "Resultado Bruto (Utilidad o P\u00e9rdida)", "Text": "4,089,068", "Tipo": "O"}, {"Codigo": "Resultado antes de participaciones e impuestos (antes de ajustes tributarios)", "Text": "2,320,540", "Tipo": "R"}, {"Codigo": "Importe pagado", "Text": "0", "Tipo": "O"}], "InformacionAl": null}, {"Anno": 2021, "Campo": [{"Codigo": "Ingresos Netos del periodo", "Text": "8,391,835", "Tipo": "O"}, {"Codigo": "Otros Ingresos declarados", "Text": "326,155", "Tipo": "O"}, {"Codigo": "Total Activos Netos", "Text": "7,768,897", "Tipo": "R"}, {"Codigo": "Cuentas Por Cobrar Comerciales - Terceros", "Text": "1,905,989", "Tipo": "O"}, {"Codigo": "Cuentas Por Cobrar Comerciales - Relacionados", "Text": null, "Tipo": "S"}, {"Codigo": "Cuentas Por Cobrar Diversas - Terceros", "Text": "48,364", "Tipo": "R"}, {"Codigo": "Cuentas Por Cobrar Diversas - Relacionados", "Text": null, "Tipo": "S"}, {"Codigo": "Cuentas por cobrar a accionistas, socios, directores", "Text": null, "Tipo": "S"}, {"Codigo": "Provisi\u00f3n por cuentas de cuentas de cobranza dudosa", "Text": null, "Tipo": "S"}, {"Codigo": "Total Cuentas por Pagar (proveedores / de terceros / a relacionados)", "Text": "1,986,879", "Tipo": "O"}, {"Codigo": "Total Pasivo", "Text": "2,829,486", "Tipo": "R"}, {"Codigo": "Total patrimonio", "Text": "4,939,411", "Tipo": "O"}, {"Codigo": "Capital social", "Text": "863,080", "Tipo": "O"}, {"Codigo": "Resultado Bruto (Utilidad o P\u00e9rdida)", "Text": "2,400,945", "Tipo": "O"}, {"Codigo": "Resultado antes de participaciones e impuestos (antes de ajustes tributarios)", "Text": "1,113,464", "Tipo": "O"}, {"Codigo": "Importe pagado", "Text": "0", "Tipo": "O"}], "InformacionAl": null}], "InformacionAl": "11/09/2023", "RentaPersonaNatural": null}, "DeclaracionesAnualesVentasIngresosESSALUD": {"InfoEcoVentasIngresosESSALUD": [{"Anno": 2019, "CampoVenta": [{"ContribucionESSALUD": "1,491", "IngresosNetos": "309,149", "Mes": "ENERO", "Ventas": "309,149"}, {"ContribucionESSALUD": "1,638", "IngresosNetos": "393,324", "Mes": "FEBRERO", "Ventas": "390,349"}, {"ContribucionESSALUD": "1,689", "IngresosNetos": "291,544", "Mes": "MARZO", "Ventas": "291,544"}, {"ContribucionESSALUD": "1,821", "IngresosNetos": "325,146", "Mes": "ABRIL", "Ventas": "325,146"}, {"ContribucionESSALUD": "1,889", "IngresosNetos": "284,817", "Mes": "MAYO", "Ventas": "284,817"}, {"ContribucionESSALUD": "1,912", "IngresosNetos": "407,791", "Mes": "JUNIO", "Ventas": "407,791"}, {"ContribucionESSALUD": "2,080", "IngresosNetos": "494,084", "Mes": "JULIO", "Ventas": "494,084"}, {"ContribucionESSALUD": "2,080", "IngresosNetos": "367,917", "Mes": "AGOSTO", "Ventas": "367,917"}, {"ContribucionESSALUD": "2,058", "IngresosNetos": "374,463", "Mes": "SETIEMBRE", "Ventas": "374,463"}, {"ContribucionESSALUD": "2,017", "IngresosNetos": "481,327", "Mes": "OCTUBRE", "Ventas": "481,327"}, {"ContribucionESSALUD": "2,134", "IngresosNetos": "305,239", "Mes": "NOVIEMBRE", "Ventas": "306,073"}, {"ContribucionESSALUD": "2,196", "IngresosNetos": "331,923", "Mes": "DICIEMBRE", "Ventas": "332,088"}], "InformacionAl": null}, {"Anno": 2021, "CampoVenta": [{"ContribucionESSALUD": "3,962", "IngresosNetos": "631,341", "Mes": "ENERO", "Ventas": "633,553"}, {"ContribucionESSALUD": "3,996", "IngresosNetos": "479,564", "Mes": "FEBRERO", "Ventas": "480,864"}, {"ContribucionESSALUD": "4,024", "IngresosNetos": "730,898", "Mes": "MARZO", "Ventas": "716,502"}, {"ContribucionESSALUD": "4,010", "IngresosNetos": "474,637", "Mes": "ABRIL", "Ventas": "474,637"}, {"ContribucionESSALUD": "4,172", "IngresosNetos": "558,165", "Mes": "MAYO", "Ventas": "559,964"}, {"ContribucionESSALUD": "4,283", "IngresosNetos": "731,051", "Mes": "JUNIO", "Ventas": "731,051"}, {"ContribucionESSALUD": "4,293", "IngresosNetos": "678,952", "Mes": "JULIO", "Ventas": "678,952"}, {"ContribucionESSALUD": "4,369", "IngresosNetos": "740,210", "Mes": "AGOSTO", "Ventas": "740,210"}, {"ContribucionESSALUD": "4,427", "IngresosNetos": "858,037", "Mes": "SETIEMBRE", "Ventas": "877,789"}, {"ContribucionESSALUD": "4,523", "IngresosNetos": "819,689", "Mes": "OCTUBRE", "Ventas": "819,809"}, {"ContribucionESSALUD": "4,591", "IngresosNetos": "862,887", "Mes": "NOVIEMBRE", "Ventas": "865,625"}, {"ContribucionESSALUD": "5,184", "IngresosNetos": "826,357", "Mes": "DICIEMBRE", "Ventas": "826,357"}], "InformacionAl": null}, {"Anno": 2022, "CampoVenta": [{"ContribucionESSALUD": "5,020", "IngresosNetos": "868,845", "Mes": "ENERO", "Ventas": "868,845"}, {"ContribucionESSALUD": "4,991", "IngresosNetos": "906,916", "Mes": "FEBRERO", "Ventas": "928,289"}, {"ContribucionESSALUD": "5,233", "IngresosNetos": "1,049,380", "Mes": "MARZO", "Ventas": "1,087,120"}, {"ContribucionESSALUD": "5,517", "IngresosNetos": "1,067,474", "Mes": "ABRIL", "Ventas": "1,073,641"}, {"ContribucionESSALUD": "5,845", "IngresosNetos": "1,307,751", "Mes": "MAYO", "Ventas": "1,307,751"}, {"ContribucionESSALUD": "6,368", "IngresosNetos": "1,352,542", "Mes": "JUNIO", "Ventas": "1,352,542"}, {"ContribucionESSALUD": "6,307", "IngresosNetos": "1,220,843", "Mes": "JULIO", "Ventas": "1,260,115"}, {"ContribucionESSALUD": "6,411", "IngresosNetos": "1,552,877", "Mes": "AGOSTO", "Ventas": "1,586,556"}, {"ContribucionESSALUD": "6,387", "IngresosNetos": "1,178,052", "Mes": "SETIEMBRE", "Ventas": "1,222,021"}, {"ContribucionESSALUD": "6,444", "IngresosNetos": "1,275,743", "Mes": "OCTUBRE", "Ventas": "1,293,423"}, {"ContribucionESSALUD": "6,351", "IngresosNetos": "1,317,622", "Mes": "NOVIEMBRE", "Ventas": "1,339,442"}, {"ContribucionESSALUD": "6,341", "IngresosNetos": "1,723,009", "Mes": "DICIEMBRE", "Ventas": "1,725,437"}], "InformacionAl": null}, {"Anno": 2023, "CampoVenta": [{"ContribucionESSALUD": "6,503", "IngresosNetos": "1,200,759", "Mes": "ENERO", "Ventas": "1,215,202"}, {"ContribucionESSALUD": "6,564", "IngresosNetos": "1,349,581", "Mes": "FEBRERO", "Ventas": "1,360,932"}, {"ContribucionESSALUD": "6,352", "IngresosNetos": "1,241,724", "Mes": "MARZO", "Ventas": "1,241,724"}, {"ContribucionESSALUD": "6,859", "IngresosNetos": "1,208,477", "Mes": "ABRIL", "Ventas": "1,209,268"}, {"ContribucionESSALUD": "6,638", "IngresosNetos": "1,578,282", "Mes": "MAYO", "Ventas": "1,670,157"}, {"ContribucionESSALUD": "7,175", "IngresosNetos": "1,460,266", "Mes": "JUNIO", "Ventas": "1,504,174"}, {"ContribucionESSALUD": "7,589", "IngresosNetos": "1,499,647", "Mes": "JULIO", "Ventas": "1,612,006"}, {"ContribucionESSALUD": "7,314", "IngresosNetos": "1,810,603", "Mes": "AGOSTO", "Ventas": "1,819,702"}], "InformacionAl": null}], "InformacionAl": "18/09/2023"}, "DeclaracionesMensuales": [{"Anno": 2023, "DeclaracionMensual": [{"CategoriaRenta": 3, "Estado": "Present\u00f3", "Monto": "1,200,759", "Periodo": "ENERO", "Tipo": "O"}, {"CategoriaRenta": 3, "Estado": "Present\u00f3", "Monto": "1,349,581", "Periodo": "FEBRERO", "Tipo": "O"}, {"CategoriaRenta": 3, "Estado": "Present\u00f3", "Monto": "1,241,724", "Periodo": "MARZO", "Tipo": "O"}, {"CategoriaRenta": 3, "Estado": "Present\u00f3", "Monto": "1,208,477", "Periodo": "ABRIL", "Tipo": "O"}, {"CategoriaRenta": 3, "Estado": "Present\u00f3", "Monto": "1,578,282", "Periodo": "MAYO", "Tipo": "O"}, {"CategoriaRenta": 3, "Estado": "Present\u00f3", "Monto": "1,460,266", "Periodo": "JUNIO", "Tipo": "O"}, {"CategoriaRenta": 3, "Estado": "Present\u00f3", "Monto": "1,499,647", "Periodo": "JULIO", "Tipo": "O"}, {"CategoriaRenta": 3, "Estado": "Present\u00f3", "Monto": "1,810,603", "Periodo": "AGOSTO", "Tipo": "O"}], "InformacionAl": "18/09/2023", "Titulo": "EJERCICIO ACTUAL - INGRESOS NETOS DECLARADOS MENSUALMENTE"}], "RentasTrabajoInformadas": null}, "InfoIGVJusto": {"BeneficioIGV": [{"Acogido": false, "Periodo": "2023-05", "PublicadoPadron": true}, {"Acogido": false, "Periodo": "2023-06", "PublicadoPadron": true}, {"Acogido": false, "Periodo": "2023-07", "PublicadoPadron": true}, {"Acogido": false, "Periodo": "2023-08", "PublicadoPadron": true}], "InformacionAl": "19/09/2023"}, "InfoLegal": {"Constitucion": {"Asiento": null, "FchInscripcionRRPP": "02/10/2007", "Folio": null, "NroPartidaRegistral": null, "OrigenCapital": null, "PaisOrigenCapital": null, "TomoFicha": null}, "PersonasVinculadas": null, "Representantes": null}, "InfoParticipacionPatrimonial": [{"Anno": 2022, "Socio": [{"Documento": "DNI", "FechaConstitucionSocio": "30/08/2009", "Nombre": "LOPEZ HERRERA LUIS HERNAN", "Numero": "10284638", "ParticipacionCapital": 50.0, "Tipo": "Persona Natural Domiciliada"}, {"Documento": "DNI", "FechaConstitucionSocio": "26/09/2007", "Nombre": "MOLINA SARMIENTO RINA SOLANS", "Numero": "41613604", "ParticipacionCapital": 50.0, "Tipo": "Persona Natural Domiciliada"}]}, {"Anno": 2021, "Socio": [{"Documento": "DNI", "FechaConstitucionSocio": "30/08/2009", "Nombre": "LOPEZ HERRERA LUIS HERNAN", "Numero": "10284638", "ParticipacionCapital": 50.0, "Tipo": "Persona Natural Domiciliada"}, {"Documento": "DNI", "FechaConstitucionSocio": "26/09/2007", "Nombre": "MOLINA SARMIENTO RINA SOLANS", "Numero": "41613604", "ParticipacionCapital": 50.0, "Tipo": "Persona Natural Domiciliada"}]}], "InfoRegimenesEspeciales": {"Error": null, "RegimenEspecial": [{"AcogidoNRUS": null, "AcogidoRER": null, "Anno": 2022}, {"AcogidoNRUS": null, "AcogidoRER": null, "Anno": 2021}]}, "InfoTrabajadores": {"Empleados": [{"NroTrabajadoresDependientes4Cat": 3, "NroTrabajadoresDependientes5Cat": 20, "Pensionistas": 0, "Periodo": "2023-08", "PrestadoresServicio": 0, "Trabajadores": 0}, {"NroTrabajadoresDependientes4Cat": 5, "NroTrabajadoresDependientes5Cat": 17, "Pensionistas": 0, "Periodo": "2022-08", "PrestadoresServicio": 0, "Trabajadores": 0}], "InformacionAl": "18/09/2023"}, "Periodo": null}}}'
if data is not None:
    
        data_json=json.loads(data)
        tipoDocumento=data_json.get('tipoDocumento')
        fechaProceso=data_json.get('fechaProceso')
        ruc=data_json.get('ruc')
        if tipoDocumento=='fichaRuc': ##En caso sea una Ficha RUC se guarda en las tablas Ficha_RUC, caso contrario solamente se guarda el registro en Resp_Webhook

            
            # Usando pyodbc o cualquier otra biblioteca de SQL para Python
            query = """SELECT RazonSocial, TipoContribuyente, FechaInscripcion, FechaInicioActividades, EstadoConstribuyente,
                  DependenciaSUNAT, CondicionDomicilioFiscal, EmisorElectronicoDesde, Tamanno 
                  FROM BD_Datamart.[dbo].[FichaRUC_InfoGeneral]
                  WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()


            # Preparar datos para FichaRUC_InfoGeneral
            info_general_headers = ["RazonSocial", "TipoContribuyente", "FechaInscripcion", "FechaInicioActividades", 
                        "EstadoConstribuyente", "DependenciaSUNAT", "CondicionDomicilioFiscal", 
                        "EmisorElectronicoDesde", "Tamanno"]
            info_general_data = [info_general_headers]
            for row in results:
                info_general_data.append(list(row)[2:])

            # Comprobantes electrónicos
            query = """SELECT FechaActualizacion,RUC,Tipo,Desde from BD_Datamart.[dbo].[FichaRUC_ComprobantesElectronicos]  WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()


            # Preparar datos para FichaRUC_ComprobantesElectronicos
            comprobantes_headers = ["Tipo", "Desde"]
            comprobantes_data = [comprobantes_headers]
            for item in results:
                comprobantes_data.append(list(item)[2:])

            ##Inserciones a tabla FichaRUC_TributosAfectos	

            query = """SELECT FechaActualizacion,RUC,Tributo,AfectoDesde, Exoneracion_Marca,Exoneracion_Desde,Exoneracion_Hasta FROM BD_Datamart.[dbo].[FichaRUC_TributosAfectos] WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()

            # Preparar datos para FichaRUC_TributosAfectos
            tributos_headers = ["Tributo", "AfectoDesde", "Exoneracion_Marca", "Exoneracion_Desde", "Exoneracion_Hasta"]
            tributos_data = [tributos_headers]
            for item in results:
                tributos_data.append(list(item)[2:])

            ##Insercion a tabla FichaRUC_DatosContribuyente	

            query = """SELECT FechaActualizacion,RUC,NombreComercial,Tipo, ActividadEconomicaPrincipal,ActividadEconomicaSecundaria1,ActividadEconomicaSecundaria2,SistemaEmisionComprobantes, SistemaContabilidad,CodigoProfesionOficio,ActividadComercioExterior,NumeroFAX,TelefonoFijo1,TelefonoFijo2,TelefonoMovil1,TelefonoMovil2,CorreoElectronico1,CorreoElectronico2 FROM BD_Datamart.[dbo].[FichaRUC_DatosContribuyente] WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()
            
            # Preparar datos para FichaRUC_DatosContribuyente
            contribuyente_headers = ["NombreComercial", "Tipo", "ActividadEconomicaPrincipal", 
                         "ActividadEconomicaSecundaria1", "ActividadEconomicaSecundaria2", 
                         "SistemaEmisionComprobantes", "SistemaContabilidad", "CodigoProfesionOficio", 
                         "ActividadComercioExterior", "NumeroFAX", "TelefonoFijo1", "TelefonoFijo2", 
                         "TelefonoMovil1", "TelefonoMovil2", "CorreoElectronico1", "CorreoElectronico2"]
            contribuyente_data = [contribuyente_headers]
            for item in results:
                contribuyente_data.append(list(item)[2:])


            ##Insercion a tabla FichaRUC_DomicilioFiscal
            
            query = """SELECT FechaActualizacion,RUC,ActividadEconomica,Departamento, Provincia,Distrito,TipoYNombreZona,TipoYNombreVia, Nro,Km,Mz,Lote,Dpto,Interior,OtrasReferencias,CondicionDomicilioFiscal FROM BD_Datamart.[dbo].[FichaRUC_DomicilioFiscal] WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()

            # Preparar datos para FichaRUC_DomicilioFiscal
            domicilio_fiscal_headers = ["ActividadEconomica", "Departamento", "Provincia", "Distrito", "TipoYNombreZona", "TipoYNombreVia", "Nro", "Km", "Mz", "Lote", "Dpto", "Interior", "OtrasReferencias", "CondicionDomicilioFiscal"]
            domicilio_fiscal_data = [domicilio_fiscal_headers]
            for item in results:
                domicilio_fiscal_data.append(list(persona)[2:])


            ##Insercion a tabla FichaRUC_DatosEmpresa


            query = """SELECT FechaActualizacion,RUC,FechaInscripcionRRPP,NumeroPartidaRegistral,Tomo,Folio,Asiento,OrigenCapital,PaisOrigenCapital
 FROM BD_Datamart.[dbo].[FichaRUC_DatosEmpresa] WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()

            # Preparar datos para FichaRUC_DatosEmpresa
            datos_empresa_headers = ["FechaInscripcionRRPP", "NumeroPartidaRegistral", "Tomo", "Folio", "Asiento", "OrigenCapital", "PaisOrigenCapital"]
            datos_empresa_data = [datos_empresa_headers]
            for item in results:
                datos_empresa_data.append(list(item)[2:])

              
            query = """SELECT FechaActualizacion,RUC,TipoYNumeroDocumento, NombreYApellidos,Cargo,FechaNacimiento,FechaDesde, NroOrdenRepresentacion,Direccion,Ubigeo,Telefono,Correo FROM BD_Datamart.[dbo].[FichaRUC_RepresentantesLegales]  WHERE FechaActualizacion = ? AND RUC = ? """
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()
                    # Preparar datos para FichaRUC_RepresentantesLegales
            representantes_headers = ["TipoYNumeroDocumento", "NombreYApellidos", "Cargo", "FechaNacimiento", "FechaDesde", "NroOrdenRepresentacion", "Direccion", "Ubigeo", "Telefono", "Correo"]
            representantes_data = [representantes_headers]
            for representante in results:
                representantes_data.append(representante(item)[2:])


            ##Inserciones a tabla FichaRUC_OtrasPersonasVinculadas

            query = """SELECT FechaActualizacion,RUC,TipoYNumeroDocumento, NombreYApellidos,Vinculo,FechaNacimiento,FechaDesde, Origen,Porcentaje,Direccion,Ubigeo,Telefono,Correo FROM BD_Datamart.[dbo].[FichaRUC_OtrasPersonasVinculadas] WHERE FechaActualizacion = ? AND RUC = ? """
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()

            # Preparar datos para FichaRUC_OtrasPersonasVinculadas
            otras_personas_headers = ["TipoYNumeroDocumento", "NombreYApellidos", "Vinculo", "FechaNacimiento", "FechaDesde", "Origen", "Porcentaje", "Direccion", "Ubigeo", "Telefono", "Correo"]
            otras_personas_data = [otras_personas_headers]
            for persona in results:
                otras_personas_data.append(list(persona)[2:])


            ##Inserciones a tabla FichaRUC_Anexos
            
            query = """SELECT FechaActualizacion,RUC,Codigo,Tipo,Denominacion,Ubigeo,Domicilio,OtrasReferencias,CondLegal FROM BD_Datamart.[dbo].[FichaRUC_Anexos]  WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()
                    # Preparar datos para FichaRUC_Anexos
            anexos_headers = ["Codigo", "Tipo", "Denominacion", "Ubigeo", "Domicilio", "OtrasReferencias", "CondLegal"]
            anexos_data = [anexos_headers]
            for anexo in anexos:
                anexos_data.append(list(anexo)[2:])                    
 
            file_name=f"C:\\PDFPruebas\\{ruc}_FICHARUC.pdf"
            titulos = ["Información General", "Comprobantes Electrónicos","Tributos Afectos","Datos Contribuyente","Domicilio Fiscal","Datos Empresa","Representantes Legales","Otras personas vinculadas","Anexos"]
            crear_pdf("Ficha RUC",[info_general_data, comprobantes_data,tributos_data,contribuyente_data,domicilio_fiscal_data,datos_empresa_data,representantes_data,otras_personas_data,anexos_data],titulos, file_name)


        elif tipoDocumento=='reporteTributario': ##En caso sea un Reporte Tributario
           
            query = """SELECT FechaReporte,RUC,RazonSocial,NombreComercial,NombreDireccion,Departamento,Provincia,Distrito,CompPago1,CompPago2,CompPago3,FchInscripcionRRPP,FchInicioActividad,EstadoContribuyenteSUNAT,DependenciaSUNAT,SistemaContabilidad FROM BD_DATAMART.DBO.INFOGENERAL_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()

            # Preparar datos para INFOGENERAL
            info_general_headers = ["FechaReporte","RUC", "RazonSocial","NombreComercial","NombreDireccion","Departamento","Provincia","Distrito","CompPago1","CompPago2","CompPago3","FchInscripcionRRPP","FchInicioActividad","EstadoContribuyenteSUNAT","DependenciaSUNAT","SistemaContabilidad"]
            info_general_data = [info_general_headers]

            # Transformar los resultados de la consulta en listas
            for row in results:
                info_general_data.append(list(row))

            transposed_info_general_data = [list(row) for row in zip(*info_general_data)]

            ###INFO. ACTIVIDAD COMERCIAL
            query = """SELECT FechaReporte,RUC,RazonSocial, Glosa, Acteco FROM BD_DATAMART.DBO.ACTCOMERCIAL_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()
            
            # Preparar datos para ACTECOS
            actecos_headers = ["Glosa","Acteco"]  # y el resto de tus columnas
            actecos_data = [actecos_headers]
            
            for row in results:
                actecos_data.append(list(row)[2:])

            ###INFO. CPE SISTEMAS
            query = """SELECT FechaReporte,RUC,RazonSocial, desde,texto FROM BD_DATAMART.DBO.CPESISTEMAS_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()
          
            # Preparar datos para CPE SISTEMAS
            cpesis_headers = ["desde","texto"]  # y el resto de tus columnas
            cpesis_data = [cpesis_headers]
            for row in results:
                cpesis_data.append(list(row)[2:])
            
            ###INFO. DECLARACIONES ANUALES        
            query = """SELECT FechaReporte,RUC,anno, codigo,tipo, texto, FechaReporte FROM BD_DATAMART.DBO.DECA_INFOECO_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()
 
            # Preparar datos para DEC ANUAL
            deca_headers = [ "anno","codigo","tipo","texto"]  # y el resto de tus columnas
            deca_data = [deca_headers]
            for row in results:
                deca_data.append(list(row)[2:])
                  
            ###INFO. DECLARACIONES MENSUALES  
            query = """SELECT FechaReporte,RUC,anno,periodo,tipo, estado,monto FROM BD_DATAMART.DBO.DECMEN_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()

             # Preparar datos para DEC MEN
            decmen_headers = ["anno","periodo","tipo","estado", "monto"]  # y el resto de tus columnas
            decmen_data = [decmen_headers]
            for row in results:
                decmen_data.append(list(row)[2:])
                
            ###INFO. ESSALUD  
            query = """SELECT FechaReporte,RUC,anno,Mes,Ventas,IngresosNetos,ContribucionESSALUD FROM BD_DATAMART.DBO.DECESSALUD_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()
           
             # Preparar datos para DEC ESSALUD
            decessalud_headers = [ "anno","Mes","Ventas","IngresosNetos", "ContribucionESSALUD"]  # y el resto de tus columnas
            decessalud_data = [decessalud_headers]
            for row in results:
                decessalud_data.append(list(row)[2:])
    
            ###INFO. REGIMEN ESPECIAL
            query = """SELECT FechaReporte,RUC,anno,AzogidoRER,AcogidoNRUS FROM BD_DATAMART.DBO.REGESPECIAL_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()
           
            # Preparar datos para REG ESPECIAL
            regespecial_headers = ["anno","AzogidoRER","AcogidoNRUS"]  # y el resto de tus columnas
            regespecial_data = [regespecial_headers]
            for row in results:
                regespecial_data.append(list(row)[2:])
                
    
            ###INFO. PARTICIPACION PATRIMONIAL
        
            query = """SELECT FechaReporte, RUC, Tipo, Nombre, Documento, Numero, ParticipacionCapital, FechaConstitucionSocio FROM BD_DATAMART.DBO.INFOPATRIMONIAL_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()
            
            # Preparar datos para INFO PATRIMONIAL
            patrimonial_headers = ["Tipo","Nombre","Documento", "Numero", "ParticipacionCapital","FechaConstitucionSocio"]  # y el resto de tus columnas
            patrimonial_data = [patrimonial_headers]
            for row in results:
                patrimonial_data.append(list(row)[2:])
        
            ###INFO. IGV JUSTO
            
            query = """SELECT FechaReporte, RUC, periodo, PublicadoPadron, Acogido FROM BD_DATAMART.DBO.IGVJUSTO_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()  
        
            # Preparar datos para IGV JUSTO
            igv_headers = ["periodo","PublicadoPadron","Acogido"]  # y el resto de tus columnas
            igv_data = [igv_headers]
            for row in results:
                igv_data.append(list(row)[2:])
    
            ###INFO TRABAJADORES
            query = """SELECT FechaReporte, RUC, PrimeraCat,SegundaCat, TerceraCat, CuartaCat, QuintaCat, SextaCat, Periodo FROM BD_DATAMART.DBO.TRABAJADORES_RTT WHERE FechaActualizacion = ? AND RUC = ?"""
            cursor.execute(query, fechaProceso, ruc)
            results = cursor.fetchall()  
      
            # Preparar datos para TRABAJADORES
            trabajadores_headers = [ "PrimeraCat","SegundaCat","TerceraCat", "CuartaCat", "QuintaCat", "SextaCat", "Periodo"]  # y el resto de tus columnas
            trabajadores_data = [trabajadores_headers]
            for row in results:
                trabajadores_data.append(list(row)[2:])
                
            # Crear PDF
        fecha_obj = datetime.strptime(fecha_reporte, "%d/%m/%Y %H:%M")
        fecha_formateada = fecha_obj.strftime("%Y%m%d")    
        file_name=f"C:\\PDFPruebas\\{ruc}_{fecha_formateada}RTT.pdf"
        titulos = ["Información General", "Actividad Comercial","CPE Sistemas","Declaración Anual","Declaración Mensual","Declaración ESSALUD","Regimen Especial","Información Patrimonial","IGV Justo","Trabajadores"]
        crear_pdf("Reporte Tributario",[transposed_info_general_data, actecos_data,cpesis_data,deca_data,decmen_data,decessalud_data,regespecial_data,patrimonial_data,igv_data,trabajadores_data],titulos, file_name)
        
            #INSERTAR DOC EN TABLA DE DOCUMENTOS WAS
            
        
        
        
#         return jsonify({'mensaje': 'Webhook recibido correctamente'}), 200

# else:
#         cursor.close()
#         abort(400)

# if __name__ == '__main__':
#     app.run()

# webhook()


# In[ ]:




