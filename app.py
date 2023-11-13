
from flask import Flask, request, abort, jsonify
import requests
import pyodbc
import json
from datetime import datetime


app=Flask(__name__)

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

@app.route('/webhook',methods=['POST'])
def webhook():
    if(request.method == 'POST' ):
        cursor = conn.cursor()#Conectar a base de datos
        data_json=request.json ##Extraer data
        RUC=data_json.get('RUC')
        RTT=data_json.get("DatamartReport", {}).get("RTRIB", {})
        FA=datetime.now()
        print(RUC)
        if RUC is not None: ##En caso sea una Ficha RUC se guarda en las tablas Ficha_RUC, caso contrario solamente se guarda el registro en Resp_Webhook
            F_R=requests.get(data_json.get('EnlaceJson')).json() ##Acceder al json de la URL (diccionario principal)

            ##Insercion a tabla FichaRUC_InfoGeneral

            
            
            RZ=F_R.get('RazonSocial')
            TC=F_R.get('TipoContribuyente')
            FI=F_R.get('FechaInscripcion')
            FIA=F_R.get('FechaInicioActividades')
            EC=F_R.get('EstadoConstribuyente')
            DS=F_R.get('DependenciaSUNAT')
            CDF=F_R.get('CondicionDomicilioFiscal')
            EED=F_R.get('EmisorElectronicoDesde')
            T=F_R.get('Tamanno')

            
            query = """INSERT INTO BD_Datamart.[dbo].[FichaRUC_InfoGeneral] (FechaActualizacion,RUC,RazonSocial,TipoContribuyente, FechaInscripcion,
                                                        FechaInicioActividades, EstadoContribuyente, DependenciaSUNAT, 
                                                        CondicionDomicilioFiscal, EmisorElectronicoDesde, Tamanno) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, FA,RUC,RZ,TC,FI,FIA,EC,DS,CDF,EED,T)
            conn.commit()

            ##Inserciones a tabla FichaRUC_InfoGeneral

            comprobantes=F_R.get('ComprobantesElectronicos')

            if comprobantes is not None:
                for comprobante in comprobantes:
                    T=comprobante.get('Tipo')
                    D=comprobante.get('Desde')
                    query = """INSERT INTO BD_Datamart.[dbo].[FichaRUC_ComprobantesElectronicos] (FechaActualizacion,RUC,Tipo,Desde) 
                        VALUES (?, ?, ?, ?)"""
                    cursor.execute(query, FA,RUC,T,D)
                    conn.commit()



            ##Inserciones a tabla FichaRUC_TributosAfectos	
            tributos=F_R.get('TributosAfectos')

            if tributos is not None:
                for tributo in tributos:
                    T=tributo.get('Tributo')
                    AD=tributo.get('AfectoDesde')
                    E_M=tributo.get('Exoneracion').get('Marca')
                    E_D=tributo.get('Exoneracion').get('Desde')
                    E_H=tributo.get('Exoneracion').get('Hasta')
                    query = """INSERT INTO BD_Datamart.[dbo].[FichaRUC_TributosAfectos] (FechaActualizacion,RUC,Tributo,AfectoDesde,
                                                                                        Exoneracion_Marca,Exoneracion_Desde,Exoneracion_Hasta) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)"""
                    cursor.execute(query, FA,RUC,T,AD,E_M,E_D,E_H)
                    conn.commit()


            ##Insercion a tabla FichaRUC_DatosContribuyente	


            NC=F_R.get('DatosContribuyente').get('NombreComercial')
            T=F_R.get('DatosContribuyente').get('Tipo')
            AEP=F_R.get('DatosContribuyente').get('ActividadEconomicaPrincipal')
            AES1=F_R.get('DatosContribuyente').get('ActividadEconomicaSecundaria1')
            AES2=F_R.get('DatosContribuyente').get('ActividadEconomicaSecundaria2')
            SEC=F_R.get('DatosContribuyente').get('SistemaEmisionComprobantes')
            SC=F_R.get('DatosContribuyente').get('SistemaContabilidad')
            CPO=F_R.get('DatosContribuyente').get('CodigoProfesionOficio')
            ACE=F_R.get('DatosContribuyente').get('ActividadComercioExterior')
            NF=F_R.get('DatosContribuyente').get('NumeroFAX')
            TF1=F_R.get('DatosContribuyente').get('TelefonoFijo1')
            TF2=F_R.get('DatosContribuyente').get('TelefonoFijo2')
            TM1=F_R.get('DatosContribuyente').get('TelefonoMovil1')
            TM2=F_R.get('DatosContribuyente').get('TelefonoMovil2')
            CE1=F_R.get('DatosContribuyente').get('CorreoElectronico1')
            CE2=F_R.get('DatosContribuyente').get('CorreoElectronico2')

            query = """INSERT INTO BD_Datamart.[dbo].[FichaRUC_DatosContribuyente] (FechaActualizacion,RUC,NombreComercial,Tipo,
                                                                                ActividadEconomicaPrincipal,ActividadEconomicaSecundaria1,
                                                                                ActividadEconomicaSecundaria2,SistemaEmisionComprobantes,
                                                                                SistemaContabilidad,CodigoProfesionOficio,ActividadComercioExterior,
                                                                                NumeroFAX,
                                                                                TelefonoFijo1,TelefonoFijo2,TelefonoMovil1,TelefonoMovil2,
                                                                                CorreoElectronico1,CorreoElectronico2) 
                    VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?)"""
            cursor.execute(query, FA,RUC,NC,T,AEP,AES1,AES2,SEC,SC,CPO,ACE,NF,TF1,TF2,TM1,TM2,CE1,CE2)
            conn.commit()

            ##Insercion a tabla FichaRUC_DomicilioFiscal

            AE=F_R.get('DomicilioFiscal').get('ActividadEconomica')
            DEP=F_R.get('DomicilioFiscal').get('Departamento')
            P=F_R.get('DomicilioFiscal').get('Provincia')
            DIS=F_R.get('DomicilioFiscal').get('Distrito')
            TYNZ=F_R.get('DomicilioFiscal').get('TipoYNombreZona')
            TYNV=F_R.get('DomicilioFiscal').get('TipoYNombreVia')
            NRO=F_R.get('DomicilioFiscal').get('Nro')
            KM=F_R.get('DomicilioFiscal').get('Km')
            MZ=F_R.get('DomicilioFiscal').get('Mz')
            LT=F_R.get('DomicilioFiscal').get('Lote')
            DPTO=F_R.get('DomicilioFiscal').get('Dpto')
            INT=F_R.get('DomicilioFiscal').get('Interior')
            OR=F_R.get('DomicilioFiscal').get('OtrasReferencias')
            CDF=F_R.get('DomicilioFiscal').get('CondicionDomicilioFiscal')

            query = """INSERT INTO BD_Datamart.[dbo].[FichaRUC_DomicilioFiscal] (FechaActualizacion,RUC,ActividadEconomica,Departamento,
                                                                                    Provincia,Distrito,TipoYNombreZona,TipoYNombreVia,
                                                                                    Nro,Km,Mz,Lote,Dpto,Interior,OtrasReferencias,
                                                                                    CondicionDomicilioFiscal) 
                    VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?)"""
            cursor.execute(query, FA,RUC,AE,DEP,P,DIS,TYNZ,TYNV,NRO,KM,MZ,LT,DPTO,INT,OR,CDF)
            conn.commit()


            ##Insercion a tabla FichaRUC_DatosEmpresa

            FIRRPP=F_R.get('DatosEmpresa').get('FechaInscripcionRRPP')
            NPR=F_R.get('DatosEmpresa').get('NumeroPartidaRegistral')
            T=F_R.get('DatosEmpresa').get('Tomo')
            F=F_R.get('DatosEmpresa').get('Folio')
            A=F_R.get('DatosEmpresa').get('Asiento')
            OC=F_R.get('DatosEmpresa').get('OrigenCapital')
            POC=F_R.get('DatosEmpresa').get('PaisOrigenCapital')

            query = """INSERT INTO BD_Datamart.[dbo].[FichaRUC_DatosEmpresa] (FechaActualizacion,RUC,FechaInscripcionRRPP,NumeroPartidaRegistral,
                                                                            Tomo,Folio,Asiento,OrigenCapital,PaisOrigenCapital) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, FA,RUC,FIRRPP,NPR,T,F,A,OC,POC)
            conn.commit()

            ##Inserciones a tabla FichaRUC_DatosEmpresa
            representantes=F_R.get('RepresentantesLegales')

            if representantes is not None:
                for representante in representantes:
                    TYND=representante.get('TipoYNumeroDocumento')
                    NYA=representante.get('NombreYApellidos')
                    CAR=representante.get('Cargo')
                    FN=representante.get('FechaNacimiento')
                    FD=representante.get('FechaDesde')
                    NOR=representante.get('NroOrdenRepresentacion')
                    D=representante.get('Direccion')
                    U=representante.get('Ubigeo')
                    T=representante.get('Telefono')
                    COR=representante.get('Correo')
                
                    query = """INSERT INTO BD_Datamart.[dbo].[FichaRUC_RepresentantesLegales] (FechaActualizacion,RUC,TipoYNumeroDocumento,
                                                                                            NombreYApellidos,Cargo,FechaNacimiento,FechaDesde,
                                                                                            NroOrdenRepresentacion,Direccion,Ubigeo,Telefono,
                                                                                            Correo) 
                        VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?,?,?)"""
                    cursor.execute(query, FA,RUC,TYND,NYA,CAR,FN,FD,NOR,D,U,T,COR)
                    conn.commit()


            ##Inserciones a tabla FichaRUC_OtrasPersonasVinculadas
            
            otraspersonas=F_R.get('OtrasPersonasVinculadas')

            if otraspersonas is not None:
                for persona in otraspersonas:
                    TYND=persona.get('TipoYNumeroDocumento')
                    NYA=persona.get('NombreYApellidos')
                    V=persona.get('Vinculo')
                    FN=persona.get('FechaNacimiento')
                    FD=persona.get('FechaDesde')
                    O=persona.get('Origen')
                    P=persona.get('Porcentaje')
                    D=persona.get('Direccion')
                    U=persona.get('Ubigeo')
                    T=persona.get('Telefono')
                    COR=persona.get('Correo')
                
                    query = """INSERT INTO BD_Datamart.[dbo].[FichaRUC_OtrasPersonasVinculadas] (FechaActualizacion,RUC,TipoYNumeroDocumento,
                                                                                            NombreYApellidos,Vinculo,FechaNacimiento,FechaDesde,
                                                                                            Origen,Porcentaje,Direccion,Ubigeo,Telefono,
                                                                                            Correo) 
                        VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?)"""
                    cursor.execute(query, FA,RUC,TYND,NYA,V,FN,FD,O,P,D,U,T,COR)
                    conn.commit()

            ##Inserciones a tabla FichaRUC_Anexos
            
            anexos=F_R.get('Anexos')

            if anexos is not None:
                for anexo in anexos:
                    C=anexo.get('Codigo')
                    T=anexo.get('Tipo')
                    D=anexo.get('Denominacion')
                    U=anexo.get('Ubigeo')
                    DOM=anexo.get('Domicilio')
                    OR=anexo.get('OtrasReferencias')
                    CL=anexo.get('CondLegal')

                
                    query = """INSERT INTO BD_Datamart.[dbo].[FichaRUC_Anexos] (FechaActualizacion,RUC,Codigo,Tipo,Denominacion,Ubigeo,Domicilio,
                                                                                OtrasReferencias,CondLegal) 
                        VALUES (?, ?, ?, ?, ?, ?, ?,?,?)"""
                    cursor.execute(query, FA,RUC,C,T,D,U,DOM,OR,CL)
                    conn.commit()

        elif RTT is not None: ##En caso sea un Reporte Tributario
            parsed_data_infogral = []
            info_empresa = RTT.get("InfoEmpresa", {})
            identificacion = info_empresa.get("Identificacion", {})
            localizacion = info_empresa.get("Localizacion", {})
            direccion = localizacion.get("Direcciones", {})[0]
            caracteristicas = info_empresa.get("Caracteristicas", {})
            comp_pagos = caracteristicas.get("CompPagos", {}).get("CompPago", [])
            info_legal = RTT.get("InfoLegal", {})
            caracteristicas_tributarias = RTT.get("CaracteristicasTributarias", {})

            parsed_data_infogral.append({
                "FechaReporte": RTT.get("Fecha"),
                "RUC": identificacion.get("RUC"),
                "RazonSocial": identificacion.get("RazonSocial"),
                "NombreComercial": identificacion.get("NombreComercial"),
                "NombreDireccion": direccion.get("Nombre"),
                "Departamento": direccion.get("Departamento"),
                "Provincia": direccion.get("Provincia"),
                "Distrito": direccion.get("Distrito"),
                "CompPago1": comp_pagos[0] if len(comp_pagos) > 0 else None,
                "CompPago2": comp_pagos[1] if len(comp_pagos) > 1 else None,
                "CompPago3": comp_pagos[2] if len(comp_pagos) > 2 else None,
                "FchInscripcionRRPP": info_legal.get("Constitucion", {}).get("FchInscripcionRRPP"),
                "FchInicioActividad": caracteristicas_tributarias.get("FchInicioActividad"),
                "EstadoContribuyenteSUNAT": caracteristicas_tributarias.get("EstadoContribuyenteSUNAT", {}).get("ContribuyenteEstado"),
                "DependenciaSUNAT": caracteristicas_tributarias.get("DependenciaSUNAT", {}).get("Nombre"),
                "SistemaContabilidad": caracteristicas_tributarias.get("SLEPLE", {}).get("SistemaContabilidad")
            })
            
            insertar_en_tabla("BD_DATAMART.DBO.INFOGENERAL_RTT", parsed_data_infogral, cursor)


            ###INFO. ACTIVIDAD COMERCIAL
            parsed_data_actcom = []
            info_empresa = RTT.get("InfoEmpresa", {})
            identificacion = info_empresa.get("Identificacion", {})
            actecos_data = info_empresa.get("Caracteristicas", {}).get("Actecos", [])

            for acteco in actecos_data:
                parsed_data_actcom.append({
                    "FechaReporte": RTT.get("Fecha"),
                    "RUC": identificacion.get("RUC"),
                    "RazonSocial": identificacion.get("RazonSocial"),
                    "Glosa": acteco.get("Glosa"),
                    "Acteco": acteco.get("Acteco")[0]
                })
            insertar_en_tabla("BD_DATAMART.DBO.ACTCOMERCIAL_RTT", parsed_data_actcom, cursor)

            ###INFO. CPE SISTEMAS
            parsed_data_cpesis = []
            cpe_sistemas_data = RTT.get("CaracteristicasTributarias", {}).get("CPE", {}).get("Sistema", [])

            for cpe in cpe_sistemas_data:
                parsed_data_cpesis.append({
                    "FechaReporte": RTT.get("Fecha"),
                    "RUC": identificacion.get("RUC"),
                    "RazonSocial": identificacion.get("RazonSocial"),
                    "desde": cpe.get("Desde"),
                    "texto": cpe.get("Text")
                })
            insertar_en_tabla("BD_DATAMART.DBO.CPESISTEMAS_RTT", parsed_data_cpesis, cursor)
            
            ###INFO. DECLARACIONES ANUALES            
            parsed_data_deca=[]
            entity_type = RTT.get("InfoFinanciera", {}).get("DeclaracionesAnuales", {}).get("InfoEcoFin")
            for ecofin in entity_type:

                
                
                property_list = ecofin.get("Campo")
                for property_list_element in property_list:
                    parsed_data_deca.append({
                        "RazonSocial": identificacion.get("RazonSocial"),
                        "RUC": identificacion.get("RUC"),
                        "anno" : ecofin.get("Anno"),
                        "codigo" : property_list_element.get("Codigo"),
                        "tipo" : property_list_element.get("Tipo"),
                        "texto" : property_list_element.get("Text"),
                        "FechaReporte" : RTT.get("Fecha")
                    })
            insertar_en_tabla("BD_DATAMART.DBO.DECA_INFOECO_RTT", parsed_data_deca, cursor)
                  
            ###INFO. DECLARACIONES MENSUALES  
            parsed_data_decmen = []
            schema_data = RTT
            entity_type_data = schema_data.get("InfoFinanciera", {}).get("DeclaracionesMensuales", {})
    
            if isinstance(entity_type_data, list):
                for entity in entity_type_data:
                    property_list = entity.get("DeclaracionMensual", [])
                    for prop in property_list:
                        parsed_data_decmen.append({
                            "FechaReporte": RTT.get("Fecha"),
                            "RUC": identificacion.get("RUC"),
                            "RazonSocial": identificacion.get("RazonSocial"),
                            "anno": entity.get("Anno"),
                            "periodo": prop.get("Periodo"),
                            "tipo": prop.get("Tipo"),
                            "estado": prop.get("Estado"),
                            "monto": prop.get("Monto")
                        })
            elif isinstance(entity_type_data, dict):  # Handle if there's only one entity
                property_list = entity_type_data.get("DeclaracionMensual", [])
                for prop in property_list:
                    parsed_data_decmen.append({
                        "FechaReporte": RTT.get("Fecha"),
                        "RUC": identificacion.get("RUC"),
                        "RazonSocial": identificacion.get("RazonSocial"),
                        "anno": entity_type_data.get("Anno"),
                        "periodo": prop.get("Periodo"),
                        "tipo": prop.get("Tipo"),
                        "estado": prop.get("Estado"),
                        "monto": prop.get("Monto")
                    })
            
            insertar_en_tabla("BD_DATAMART.DBO.DECMEN_RTT", parsed_data_decmen, cursor)

            
            ###INFO. ESSALUD  
            parsed_data_essalud=[]
            schema_data = RTT
            entity_type_data = schema_data.get("InfoFinanciera", {}).get("DeclaracionesAnualesVentasIngresosESSALUD", {}).get("InfoEcoVentasIngresosESSALUD", {})
    
            if isinstance(entity_type_data, list):
                for entity in entity_type_data:
                    property_list = entity.get("CampoVenta", [])
                    for prop in property_list:
                        parsed_data_essalud.append({
                            "FechaReporte": RTT.get("Fecha"),
                            "RUC": identificacion.get("RUC"),
                            "RazonSocial": identificacion.get("RazonSocial"),
                            "anno": entity.get("Anno"),
                            "Mes": prop.get("Mes"),
                            "Ventas": prop.get("Ventas"),
                            "IngresosNetos": prop.get("IngresosNetos"),
                            "ContribucionESSALUD": prop.get("ContribucionESSALUD")
                        })
            elif isinstance(entity_type_data, dict):  # Handle if there's only one entity
                property_list = entity_type_data.get("CampoVenta", [])
                for prop in property_list:
                    parsed_data_essalud.append({
                        "FechaReporte": RTT.get("Fecha"),
                        "RUC": identificacion.get("RUC"),
                        "RazonSocial": identificacion.get("RazonSocial"),
                        "anno": entity_type_data.get("Anno"),
                        "Mes": prop.get("Mes"),
                        "Ventas": prop.get("Ventas"),
                        "IngresosNetos": prop.get("IngresosNetos"),
                        "ContribucionESSALUD": prop.get("ContribucionESSALUD")
                    })
            
            insertar_en_tabla("BD_DATAMART.DBO.DECESSALUD_RTT", parsed_data_essalud, cursor)            
    
            ###INFO. REGIMEN ESPECIAL
            parsed_data_regespecial=[]
            fecha_reporte = RTT.get("Fecha")
            ruc = identificacion.get("RUC")
            razon_social = identificacion.get("RazonSocial")

            regimen_especial = RTT.get("InfoRegimenesEspeciales", {}).get("RegimenEspecial", {})

            for regimen in regimen_especial:
                anno = regimen.get("Anno")
                acogido_rerus = regimen.get("AcogidoRER")
                acogido_nrus = regimen.get("AcogidoNRUS")

                parsed_data_regespecial.append({
                "FechaReporte": fecha_reporte,
                "RUC": ruc,
                "RazonSocial": razon_social,
                "anno": anno,
                "AzogidoRER": acogido_rerus,
                "AcogidoNRUS": acogido_nrus
                })
            

            
            insertar_en_tabla("BD_DATAMART.DBO.REGESPECIAL_RTT", parsed_data_regespecial, cursor)            

    
            ###INFO. PARTICIPACION PATRIMONIAL
            parsed_data_patrimonial=[]
            participaciones = RTT.get("InfoParticipacionPatrimonial", {})

            for participacion in participaciones:
                socios = participacion.get("Socio", {})
                for socio in socios:
                    tipo = socio.get("Tipo")
                    nombre = socio.get("Nombre")
                    documento = socio.get("Documento")
                    numero = socio.get("Numero")
                    participacion_capital = socio.get("ParticipacionCapital")
                    fecha_constitucion_socio = socio.get("FechaConsitucionSocio")
                    
                    parsed_data_patrimonial.append({
                    "FechaReporte": fecha_reporte,
                    "RUC": ruc,
                    "RazonSocial": razon_social,
                    "Tipo": tipo,
                    "Nombre": nombre,
                    "Documento": documento,
                    "Numero": numero,
                    "ParticipacionCapital": participacion_capital,
                    "FechaConstitucionSocio": fecha_constitucion_socio
                    })


          
            insertar_en_tabla("BD_DATAMART.DBO.INFOPATRIMONIAL_RTT", parsed_data_patrimonial, cursor)            
        
            ###INFO. IGV JUSTO
            parsed_data_igv=[]
            beneficios_igv = RTT.get("InfoIGVJusto", {}).get("BeneficioIGV", {})
            for beneficio_igv in beneficios_igv:
                periodo = beneficio_igv.get("Periodo")
                publicado_padron = beneficio_igv.get("PublicadoPadron")
                acogido = beneficio_igv.get("Acogido")

                parsed_data_igv.append({
                    "FechaReporte": fecha_reporte,
                    "RUC": ruc,
                    "RazonSocial": razon_social,
                    "periodo": periodo,
                    "PublicadoPadron": publicado_padron,
                    "Acogido": acogido
                })
    
            insertar_en_tabla("BD_DATAMART.DBO.IGVJUSTO_RTT", parsed_data_igv, cursor)            

    
            ###INFO TRABAJADORES
            parsed_data_trabajadores=[]
            empleados = RTT.get("InfoTrabajadores", {}).get("Empleados", {})
            for periodo in empleados: ##OBSERVACION, NECESARIO AÑADIR COLUMNA PERIODO
                primera_cat = periodo.get("NroTrabajadoresDependientes1Cat")
                segunda_cat = periodo.get("NroTrabajadoresDependientes2Cat")
                tercera_cat = periodo.get("NroTrabajadoresDependientes3Cat")
                cuarta_cat = periodo.get("NroTrabajadoresDependientes4Cat")
                quinta_cat = periodo.get("NroTrabajadoresDependientes5Cat")
                sexta_cat = periodo.get("NroTrabajadoresDependientes6Cat")
                periodo = periodo.get("Periodo")

                parsed_data_trabajadores.append({
                    "FechaReporte": fecha_reporte,
                    "RUC": ruc,
                    "RazonSocial": razon_social,
                    "PrimeraCat": primera_cat,
                    "SegundaCat": segunda_cat,
                    "TerceraCat": tercera_cat,
                    "CuartaCat": cuarta_cat,
                    "QuintaCat": quinta_cat,
                    "SextaCat": sexta_cat,
                    "Periodo": periodo
                })
    
            insertar_en_tabla("BD_DATAMART.DBO.TRABAJADORES_RTT", parsed_data_trabajadores, cursor)   
        
        
        
        ##Inserciones a tabla [dbo].[Resp_Webhook]
        data_to_insert=json.dumps(data_json)
        print(data_to_insert)
        insert_statement = """INSERT INTO BD_Datamart.[dbo].[Resp_Webhook] (FechaRegistro,Respuesta) VALUES (?, ?)"""
        data=(FA,data_to_insert)
        cursor.execute(insert_statement, data)
        conn.commit()
        cursor.close()
        return jsonify({'mensaje': 'Webhook recibido correctamente'}), 200

    else:
        cursor.close()
        abort(400)

if __name__ == '__main__':
    app.run()



