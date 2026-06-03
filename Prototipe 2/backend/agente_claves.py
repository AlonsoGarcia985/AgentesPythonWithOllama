from config import DOCUMENTOS_REQUERIDOS

CLAVES_RAIZ = ["nombre", "rfc", "departamento", "puesto", "documentos", "fecha_inicio"]
CLAVES_ANIDADAS = {
    "departamento": ["id", "nombre"],
    "puesto": ["titulo", "nivel", "salario_base"],
    "documentos": DOCUMENTOS_REQUERIDOS,
}


def agente_claves(empleado):
    faltantes = [k for k in CLAVES_RAIZ if k not in empleado]
    if faltantes:
        return {"ok": False, "error": f"Faltan claves raíz: {faltantes}"}

    for obj, claves in CLAVES_ANIDADAS.items():
        if not isinstance(empleado.get(obj), dict):
            return {"ok": False, "error": f"'{obj}' debe ser un objeto (dict)"}
        internas = [k for k in claves if k not in empleado[obj]]
        if internas:
            return {"ok": False, "error": f"Faltan claves en '{obj}': {internas}"}

    return {"ok": True, "valor": empleado}

