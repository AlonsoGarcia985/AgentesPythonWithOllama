from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pipeline import ejecutar_pipeline
from agente_claves import agente_claves
from agente_rfc_formato import agente_rfc_formato
from agente_rfc_bd import agente_rfc_bd
from agente_departamento_bd import agente_departamento_bd
from agente_salario_bd import agente_salario_bd
from agente_documentos import agente_documentos
from agente_azure_client import agente_contrato
from agente_correo import agente_correo

app = FastAPI(title="Onboarding API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# La lista de agentes EN ORDEN. El orden importa: cada uno recibe el empleado

AGENTES = [
    agente_claves,
    agente_rfc_formato,
    agente_rfc_bd,
    agente_departamento_bd,
    agente_salario_bd,
    agente_documentos,
    agente_contrato,
    agente_correo,
]


@app.get("/")
def inicio():
    return {"mensaje": "Onboarding API funcionando. Usa POST /validar-empleado"}


@app.post("/validar-empleado")
def validar_empleado(empleado: dict):
    # FastAPI convierte el JSON del body en este dict 'empleado'.
    # Lo pasamos por el pipeline y devolvemos el resultado tal cual (JSON).
    return ejecutar_pipeline(empleado, AGENTES)
