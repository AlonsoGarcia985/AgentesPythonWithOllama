from pipeline import ejecutar_pipeline
from agente_claves import agente_claves
from agente_rfc_formato import agente_rfc_formato
from agente_rfc_duplicado import agente_rfc_duplicado
from agente_departamento import agente_departamento
from agente_salario import agente_salario
from agente_documentos import agente_documentos
from agente_contrato_ollama import agente_contrato_ollama



#  JSON DE ENTRADA — el empleado a validar (estructura anidada)

empleado_demo = {
    "nombre": "Ana Torres",
    "rfc": "TORA900315AB2",
    "departamento": {
        "id": 3,
        "nombre": "Ingeniería",
    },
    "puesto": {
        "titulo": "Desarrollador Sr",
        "nivel": "senior",
        "salario_base": 28000,
    },
    "documentos": {
        "ine": True,
        "curp": True,
        "comprobante_domicilio": True,
        "acta_nacimiento": True,
    },
    "fecha_inicio": "2024-09-01",
}


#  MAIN
if __name__ == "__main__":
    # Por ahora solo el primer agente; iremos sumando los demás.
    agentes = [
        agente_claves,
        agente_rfc_formato,
        agente_rfc_duplicado,
        agente_departamento,
        agente_salario,
        agente_documentos,
        agente_contrato_ollama,
    ]
    resultado = ejecutar_pipeline(empleado_demo, agentes)
    print(resultado["empleado"]["contrato"])

