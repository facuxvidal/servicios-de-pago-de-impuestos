from datetime import date, datetime
from fastapi import FastAPI,HTTPException,Body,Request
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime,timedelta
import random


app = FastAPI(title="Servicios de Pago de Impuestos")


class ParametrosCreaBoleta(BaseModel):
    tipo_de_servicio: str
    descripcion_servicio: str="Edenor S.A."
    fecha_de_vencimiento: date="2022-08-06"
    importe: float
    estado: str
    codigo_de_barras: int


class ParametrosRealizaPago(BaseModel):
    metodo_de_pago: str
    numero_tarjeta: Optional[str]
    importe: float
    codigo_de_barras: float
    fecha_de_pago: date="2022-07-06"


class PagosResponse(BaseModel):
    fecha_de_pago: datetime
    importe_acumulado: float
    transacciones_acumuladas: int


class ParametrosListaPagos(BaseModel):
    fecha_inicio: datetime="2022-07-06T13:00:05"
    fecha_fin: datetime="2022-07-09T13:00:05"


class ParametrosListaBoletas(BaseModel):
    tipo_de_servicio: Optional[str]


def get_pagos():
    # información de pagos, los datos de la tarjeta, el valor, etc.
    pagos = [
        {
            "nombre_impreso_tarjeta":"RAMIREZ JUAN ARIEL",
            "numero_tarjeta":"5020470001370055",
            "vencimiento_tarjeta":"04/25",
            "fecha_pago":"2022-07-06T13:00:05",
            "monto":2300,
            "tipo_de_moneda":"ARG"
        },
        {
            "nombre_impreso_tarjeta":"SILVIA GONZALEZ",
            "numero_tarjeta":"5020080001000006",
            "vencimiento_tarjeta":"05/26",
            "fecha_pago":"2022-07-06T15:00:05",
            "monto":100,
            "tipo_de_moneda":"ARG"
        },
        {
            "nombre_impreso_tarjeta":"ERIC CAMPAZZO",
            "numero_tarjeta":"4507670001000009",
            "vencimiento_tarjeta":"02/25",
            "fecha_pago":"2022-07-07T15:00:05",
            "monto":15000,
            "tipo_de_moneda":"ARG"
        },
        {
            "nombre_impreso_tarjeta":"MANUEL FERNANDEZ",
            "numero_tarjeta":"5540500001000001",
            "vencimiento_tarjeta":"12/25",
            "fecha_pago":"2022-07-08T19:10:05",
            "monto":9000,
            "tipo_de_moneda":"ARG"
        },        
        {
            "nombre_impreso_tarjeta":"FEDERICO NEWKIRK",
            "numero_tarjeta":"5540500001000004",
            "vencimiento_tarjeta":"12/24",
            "fecha_pago":"2022-07-08T13:10:05",
            "monto":400,
            "tipo_de_moneda":"ARG"
        }
    ]
    return pagos


def get_boletas():
    # representa las boletas creadas, con su status correspondiente (pending, paid, etc.)
    boletas = [
        {
            "numero_boleta":"001-413672",
            "fecha_de_vencimiento":"2022-08-06T13:00:05",
            "tipo_de_boleta":"A",
            "nombreyapellido":"Juan Ariel Ramirez",
            "dni":36728462,
            "importe":2300,
            "estado":"paid",
            "tipo_de_servicio":"agua",
            "codigo_de_barras":"6355159500"
        },
        {
            "numero_boleta":"001-546321",
            "fecha_de_vencimiento":"2022-08-06T15:00:05",
            "tipo_de_boleta":"A",
            "nombreyapellido":"Silvia Ana Gonzalez",
            "dni":13965746,
            "importe":100,
            "estado":"pending",
            "tipo_de_servicio":"luz",
            "codigo_de_barras":"8390789924"
        },
        {
            "numero_boleta":"001-990101",
            "fecha_de_vencimiento":"2022-08-07T15:00:05",
            "tipo_de_boleta":"B",
            "nombreyapellido":"Eric Emanuel Campazzo",
            "dni":40785138,
            "importe":15000,
            "estado":"paid",
            "tipo_de_servicio":"luz",
            "codigo_de_barras":"9576913324"
        },
        {
            "numero_boleta":"001-650098",
            "fecha_de_vencimiento":"2022-08-08T19:10:05",
            "tipo_de_boleta":"A",
            "nombreyapellido":"Manuel Fernandez",
            "dni":41231657,
            "importe":9000,
            "estado":"paid",
            "tipo_de_servicio":"agua",
            "codigo_de_barras":"4377426508"
        },
        {
            "numero_boleta":"002-110011",
            "fecha_de_vencimiento":"2022-08-08T13:10:05",
            "tipo_de_boleta":"C",
            "nombreyapellido":"Federico Elias Newkirk",
            "dni":39001262,
            "importe":400,
            "estado":"refused",
            "tipo_de_servicio":"gas",
            "codigo_de_barras":"4889467295"
        }
    ]
    return boletas


@app.post("/create-tax")
async def crear_boleta(request:ParametrosCreaBoleta):
    """
    1.Debe permitir crear una boleta de pago con la siguiente información, recibiendo la siguiente información:
    Tipo de servicio (Luz/Gas/etc...)
    Descripción del servicio. Ej: 'Edenor S.A.'
    Fecha de vencimiento. Ej (2021-01-15)
    Importe del servicio.
    Status del pago (pending, paid, etc.).
    Código de barra (debe ser único - PK)
    """
    boletas_acumuladas = get_boletas()
    for boleta in boletas_acumuladas:
        if int(boleta["codigo_de_barras"]) == request.codigo_de_barras:
            raise HTTPException(status_code=404, detail=f"La boleta no pudo ser creada! Ya existe boleta con codigo de barras {request.codigo_de_barras}")

    numero_random = str(random.random())
    nueva_boleta = {
                        "numero_boleta":f"001-{numero_random[2:8]}",
                        "fecha_de_vencimiento":request.fecha_de_vencimiento,
                        "tipo_de_boleta":"A",
                        "nombreyapellido":request.descripcion_servicio,
                        "dni":"",
                        "importe":request.importe,
                        "estado":request.estado,
                        "tipo_de_servicio":request.tipo_de_servicio,
                        "codigo_de_barras":request.codigo_de_barras
                    }
    boletas_acumuladas.append(nueva_boleta)
    #print(f'{boletas_acumuladas}')
    raise HTTPException(status_code=200, detail="Boleta creada exitosamente")


@app.post("/pay-tax")
async def realizar_pago(request:ParametrosRealizaPago):
    """
    2.Debe permitir realizar un pago (transacción), recibiendo la siguiente información:
    Método de pago (debit_card, credit_card o cash)
    Número de la tarjeta (solo en caso de no ser efectivo)
    Importe del pago
    Código de barra
    Fecha de pago
    """
    pagos_acumulados = get_pagos()
    if request.metodo_de_pago != "cash":
        nuevo_pago = {
                        "nombre_impreso_tarjeta":"#### #### ####",
                        "numero_tarjeta":request.numero_tarjeta,
                        "vencimiento_tarjeta":"##/##",
                        "fecha_pago":request.fecha_de_pago,
                        "monto":request.importe,
                        "tipo_de_moneda":"ARG"
                    }
    else:
        nuevo_pago = {
                        "nombre_impreso_tarjeta":"",
                        "numero_tarjeta":"",
                        "vencimiento_tarjeta":"",
                        "fecha_pago":request.fecha_de_pago,
                        "monto":request.importe,
                        "tipo_de_moneda":"ARG"
                    }
    pagos_acumulados.append(nuevo_pago)
    #print(f'{pagos_acumulados}')
    raise HTTPException(status_code=200, detail="Pago exitoso")


@app.post("/list-taxes")
async def listar_boletas(request:ParametrosListaBoletas):
    """
    3. Debe permitir listar aquellas boletas impagas en forma total o filtradas por tipo de servicio, devolviendo la siguiente información:
    Tipo de servicio (solo si se lista sin filtro)
    Fecha de vencimiento
    Importe del servicio
    Código de barra
    """
    rsp = []
    boletas = get_boletas()

    for boleta in boletas:

        if not request.tipo_de_servicio and boleta["estado"] != "paid":
            boleta_impaga = {
                                "tipo_de_servicio":boleta["tipo_de_servicio"],
                                "fecha_de_vencimiento":boleta["fecha_de_vencimiento"],
                                "importe_del_servicio":boleta["importe"],
                                "codigo_de_barras":boleta["codigo_de_barras"]
                            }
            rsp.append(boleta_impaga)
        

        if request.tipo_de_servicio:
            if boleta["tipo_de_servicio"] == request.tipo_de_servicio:
                boleta_por_servicio = {
                                        "fecha_de_vencimiento":boleta["fecha_de_vencimiento"],
                                        "importe_del_servicio":boleta["importe"],
                                        "codigo_de_barras":boleta["codigo_de_barras"]
                                    }
                rsp.append(boleta_por_servicio)

    return rsp


@app.post("/list-payments", response_model=List[PagosResponse])
async def listar_pagos(request:ParametrosListaPagos):
    """
    4. Debe permitir listar los pagos (transacciones) entre un período de fechas, acumulando por día, devolviendo la siguiente información:
    Fecha de pago
    Importe acumulado
    Cantidad de transacciones en esa fecha
    """
    rsp = []
    un_dia_despues = timedelta(hours=24)
    pagos = get_pagos()
    # if not formato_fechas: raise HTTPException(status_code=404, detail="Formato de fechas erroneo! Intente con usar el formato que se aclara en el ejemplo.")
    while request.fecha_inicio <= request.fecha_fin:
        monto_acumulado = 0
        transacciones_acumuladas = 0

        for pago in pagos:
            fecha_pago =  datetime.strptime(pago["fecha_pago"], '%Y-%m-%dT%H:%M:%S')
            
            if fecha_pago.day == request.fecha_inicio.day:
                monto_acumulado += pago["monto"]
                transacciones_acumuladas += 1

            registro_de_pago = {
                                    "fecha_de_pago":request.fecha_inicio,
                                    "importe_acumulado":monto_acumulado,
                                    "transacciones_acumuladas":transacciones_acumuladas
                                }
            
        rsp.append(registro_de_pago)

        request.fecha_inicio += un_dia_despues

    return rsp