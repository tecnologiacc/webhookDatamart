/* Create table if doesn't exists in schema */

USE Datamart;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'FichaRUC_InfoGeneral'
)
BEGIN
	CREATE TABLE FichaRUC_InfoGeneral (
    FechaActualizacion datetime NULL,
    RUC varchar(30) NULL,
    RazonSocial varchar(300) NULL,
    TipoContribuyente varchar(100) NULL,
    FechaInscripcion varchar(50) NULL,
    FechaInicioActividades varchar(50) NULL,
    EstadoContribuyente varchar(30) NULL,
    DependenciaSUNAT varchar(50) NULL,
    CondicionDomicilioFiscal varchar(30) NULL,
    EmisorElectronicoDesde varchar(50) NULL,
    Tamanno varchar(30) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'FichaRUC_ComprobantesElectronicos'
)
BEGIN
	CREATE TABLE FichaRUC_ComprobantesElectronicos (
    FechaActualizacion datetime NULL,
    RUC varchar(30) NULL,
    Tipo varchar(50) NULL,
    Desde varchar(50) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'FichaRUC_TributosAfectos'
)
BEGIN
	CREATE TABLE FichaRUC_TributosAfectos (
    FechaActualizacion datetime NULL,
    RUC varchar(30) NULL,
    Tributo varchar(50) NULL,
    AfectoDesde varchar(50) NULL,
    Exoneracion_Marca varchar(50) NULL,
    Exoneracion_Desde varchar(50) NULL,
    Exoneracion_Hasta varchar(50) NULL,
  )
 END;
 
IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'FichaRUC_DatosContribuyente'
)
BEGIN
	CREATE TABLE FichaRUC_DatosContribuyente (
    FechaActualizacion datetime NULL,
    RUC varchar(30) NULL,
    NombreComercial varchar(50) NULL,
    Tipo varchar(50) NULL,
    ActividadEconomicaPrincipal varchar(150) NULL,
    ActividadEconomicaSecundaria1 varchar(150) NULL,
    ActividadEconomicaSecundaria2 varchar(150) NULL,
    SistemaEmisionComprobantes varchar(50) NULL,
    SistemaContabilidad varchar(50) NULL,
    CodigoProfesionOficio varchar(50) NULL,
    ActividadComercioExterior varchar(50) NULL,
    NumeroFAX varchar(50) NULL,
    TelefonoFijo1 varchar(50) NULL,
    TelefonoFijo2 varchar(50) NULL,
    TelefonoMovil1 varchar(50) NULL,
    TelefonoMovil2 varchar(50) NULL,
    CorreoElectronico1 varchar(50) NULL,
    CorreoElectronico2 varchar(50) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'FichaRUC_DomicilioFiscal'
)
BEGIN
	CREATE TABLE FichaRUC_DomicilioFiscal (
    FechaActualizacion datetime NULL,
    RUC varchar(30) NULL,
    ActividadEconomica varchar(100) NULL,
    Departamento varchar(50) NULL,
    Provincia varchar(50) NULL,
    Distrito varchar(50) NULL,
    TipoYNombreZona varchar(70) NULL,
    TipoYNombreVia varchar(70) NULL,
    Nro varchar(50) NULL,
    Km varchar(50) NULL,
    Mz varchar(50) NULL,
    Lote varchar(50) NULL,
    Dpto varchar(50) NULL,
    Interior varchar(50) NULL,
    OtrasReferencias varchar(70) NULL,
    CondicionDomicilioFiscal varchar(50) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'FichaRUC_DatosEmpresa'
)
BEGIN
	CREATE TABLE FichaRUC_DatosEmpresa (
    FechaActualizacion datetime NULL,
    RUC varchar(30) NULL,
    FechaInscripcionRRPP varchar(50) NULL,
    NumeroPartidaRegistral varchar(50) NULL,
    Tomo varchar(50) NULL,
    Folio varchar(50) NULL,
    Asiento varchar(50) NULL,
    OrigenCapital varchar(50) NULL,
    PaisOrigenCapital varchar(50) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'FichaRUC_RepresentantesLegales'
)
BEGIN
	CREATE TABLE FichaRUC_RepresentantesLegales (
    FechaActualizacion datetime NULL,
    RUC varchar(30) NULL,
    TipoYNumeroDocumento varchar(50) NULL,
    NombreYApellidos varchar(70) NULL,
    Cargo varchar(50) NULL,
    FechaNacimiento varchar(50) NULL,
    FechaDesde varchar(50) NULL,
    NroOrdenRepresentacion varchar(50) NULL,
    Direccion varchar(50) NULL,
    Ubigeo varchar(70) NULL,
    Telefono varchar(50) NULL,
    Correo varchar(70) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'FichaRUC_OtrasPersonasVinculadas'
)
BEGIN
	CREATE TABLE FichaRUC_OtrasPersonasVinculadas (
    FechaActualizacion datetime NULL,
    RUC varchar(30) NULL,
    TipoYNumeroDocumento varchar(50) NULL,
    NombreYApellidos varchar(50) NULL,
    Vinculo varchar(50) NULL,
    FechaNacimiento varchar(50) NULL,
    FechaDesde varchar(50) NULL,
    Origen varchar(50) NULL,
    Porcentaje varchar(50) NULL,
    Direccion varchar(50) NULL,
    Ubigeo varchar(50) NULL,
    Telefono varchar(50) NULL,
    Correo varchar(50) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'FichaRUC_Anexos'
)
BEGIN
	CREATE TABLE FichaRUC_Anexos (
    FechaActualizacion datetime NULL,
    RUC varchar(30) NULL,
    Codigo varchar(50) NULL,
    Tipo varchar(50) NULL,
    Denominacion varchar(50) NULL,
    Ubigeo varchar(100) NULL,
    Domicilio varchar(100) NULL,
    OtrasReferencias varchar(100) NULL,
    CondLegal varchar(50) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'INFOGENERAL_RTT'
)
BEGIN
	CREATE TABLE INFOGENERAL_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    NombreComercial nvarchar(MAX) NULL,
    NombreDireccion nvarchar(MAX) NULL,
    Departamento nvarchar(MAX) NULL,
    Provincia nvarchar(MAX) NULL,
    Distrito nvarchar(MAX) NULL,
    CompPago1 nvarchar(MAX) NULL,
    CompPago2 nvarchar(MAX) NULL,
    CompPago3 nvarchar(MAX) NULL,
    FchInscripcionRRPP nvarchar(MAX) NULL,
    FchInicioActividad nvarchar(MAX) NULL,
    EstadoContribuyenteSUNAT nvarchar(MAX) NULL,
    DependenciaSUNAT nvarchar(MAX) NULL,
    SistemaContabilidad nvarchar(MAX) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'ACTCOMERCIAL_RTT'
)
BEGIN
	CREATE TABLE ACTCOMERCIAL_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    Glosa nvarchar(MAX) NULL,
    Acteco nvarchar(MAX) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'CPESISTEMAS_RTT'
)
BEGIN
	CREATE TABLE CPESISTEMAS_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    desde nvarchar(MAX) NULL,
    texto nvarchar(MAX) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'DECA_INFOECO_RTT'
)
BEGIN
	CREATE TABLE DECA_INFOECO_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    anno nvarchar(MAX) NULL,
    codigo nvarchar(MAX) NULL,
    tipo nvarchar(MAX) NULL,
    texto nvarchar(MAX) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'DECMEN_RTT'
)
BEGIN
	CREATE TABLE DECMEN_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    anno nvarchar(MAX) NULL,
    periodo nvarchar(50) NULL,
    tipo nvarchar(50) NULL,
    estado nvarchar(50) NULL,
    monto nvarchar(50) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'DECESSALUD_RTT'
)
BEGIN
	CREATE TABLE DECESSALUD_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    anno nvarchar(MAX) NULL,
    Mes nvarchar(50) NULL,
    Ventas nvarchar(50) NULL,
    IngresosNetos nvarchar(50) NULL,
    ContribucionESSALUD nvarchar(50) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'REGESPECIAL_RTT'
)
BEGIN
	CREATE TABLE REGESPECIAL_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    anno nvarchar(MAX) NULL,
    AzogidoRER nvarchar(MAX) NULL,
    AcogidoNRUS nvarchar(MAX) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'INFOPATRIMONIAL_RTT'
)
BEGIN
	CREATE TABLE INFOPATRIMONIAL_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    Tipo nvarchar(MAX) NULL,
    Nombre nvarchar(MAX) NULL,
    Documento nvarchar(MAX) NULL,
    Numero nvarchar(MAX) NULL,
    ParticipacionCapital nvarchar(MAX) NULL,
    FechaConstitucionSocio nvarchar(MAX) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'IGVJUSTO_RTT'
)
BEGIN
	CREATE TABLE IGVJUSTO_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    periodo nvarchar(MAX) NULL,
    PublicadoPadron nvarchar(MAX) NULL,
    Acogido nvarchar(MAX) NULL,
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'TRABAJADORES_RTT'
)
BEGIN
	CREATE TABLE TRABAJADORES_RTT (
    FechaReporte nvarchar(MAX) NULL,
    RUC nvarchar(MAX) NULL,
    RazonSocial nvarchar(MAX) NULL,
    PrimeraCat nvarchar(MAX) NULL,
    SegundaCat nvarchar(MAX) NULL,
    TerceraCat nvarchar(MAX) NULL,
    CuartaCat nvarchar(MAX) NULL,
    QuintaCat nvarchar(MAX) NULL,
    SextaCat nvarchar(MAX) NULL,
    Periodo nvarchar(MAX) NULL DEFAULT ('-'),
  )
END;

IF NOT EXISTS (
	SELECT *
  FROM information_schema.tables
  WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'Resp_Webhook'
)
BEGIN
	CREATE TABLE Resp_Webhook (
    FechaRegistro datetime NULL,
    Respuesta varchar(MAX) NULL,
  )
END;
