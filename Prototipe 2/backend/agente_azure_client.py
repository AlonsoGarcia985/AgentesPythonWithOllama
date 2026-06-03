from openai import AzureOpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    APIKEY,
    VERSION,
    MODEL,
)


def agente_contrato(empleado):
    prompt = f"""Genera un contrato laboral borrador formal en español para:
    - Nombre completo: {empleado['nombre']}
    - RFC: {empleado['rfc']}
    - Puesto: {empleado['puesto']['titulo']} (nivel {empleado['puesto']['nivel']})
    - Departamento: {empleado['departamento']['nombre']}
    - Salario mensual: ${empleado['puesto']['salario_base']:,} MXN
    - Fecha de inicio: {empleado['fecha_inicio']}
    Incluye: partes, objeto, duración, salario, jornada y firma.
"""

    try:
        client = AzureOpenAI(
            api_key=APIKEY,
            api_version=VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
        )
        respuesta = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
        )
        contrato = respuesta.choices[0].message.content
    except Exception as e:
        return {"ok": False, "error": f"No se pudo generar el contrato (Azure): {e}"}

    return {"ok": True, "valor": {**empleado, "contrato": contrato}}
