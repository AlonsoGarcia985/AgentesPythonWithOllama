from openai import AzureOpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    APIKEY,
    VERSION,
    MODEL,
)


def agente_correo(empleado):
    prompt = f"""Eres parte del equipo de Recursos Humanos. Redacta un CORREO
de bienvenida cálido y profesional en español para un nuevo empleado:

- Nombre: {empleado['nombre']}
- Puesto: {empleado['puesto']['titulo']}
- Departamento: {empleado['departamento']['nombre']}
- Fecha de inicio: {empleado['fecha_inicio']}

Incluye: un asunto (Subject), un saludo personalizado, una bienvenida al
equipo, la fecha de inicio y una despedida cordial. Máximo 150 palabras.
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
            max_tokens=400,
        )
        correo = respuesta.choices[0].message.content
    except Exception as e:
        return {"ok": False, "error": f"No se pudo generar el correo (Azure): {e}"}

    # enriquecemos el empleado con el correo generado
    return {"ok": True, "valor": {**empleado, "correo": correo}}
