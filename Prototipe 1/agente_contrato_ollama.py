import ollama


def agente_contrato_ollama(empleado):
    prompt = f"""
    Genera un contrato laboral borrador en español para:
    - Nombre: {empleado['nombre']}
    - Puesto: {empleado['puesto']['titulo']}
    - Departamento: {empleado['departamento']['nombre']}
    - Salario: ${empleado['puesto']['salario_base']:,} MXN
    - Fecha de inicio: {empleado['fecha_inicio']}
    Sé formal y conciso. Máximo 200 palabras.
    """
    respuesta = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    contrato = respuesta["message"]["content"]
    return {"ok": True, "valor": {**empleado, "contrato": contrato}}