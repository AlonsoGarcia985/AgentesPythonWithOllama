from DatosMOCK import DOCUMENTOS_REQUERIDOS




#  AGENTE 1 — agente_claves
#  Verifica que existan las 6 claves raíz y las claves internas
#  de los objetos anidados. Si falta alguna -> FATAL.

CLAVES_RAIZ = ["nombre", "rfc", "departamento", "puesto", "documentos", "fecha_inicio"]
CLAVES_ANIDADAS = {
    "departamento": ["id", "nombre"],
    "puesto": ["titulo", "nivel", "salario_base"],
    "documentos": DOCUMENTOS_REQUERIDOS,
}

#PRIMER AGENTE 1 AGENTE CLAVE
def agente_claves(empleado):
    # 1) claves a nivel raíz
    faltantes = [k for k in CLAVES_RAIZ if k not in empleado]
    if faltantes:
        return {"ok": False, "error": f"Faltan claves raíz: {faltantes}"}

    # 2) claves internas de cada objeto anidado
    for obj, claves in CLAVES_ANIDADAS.items():
        if not isinstance(empleado[obj], dict):
            return {"ok": False, "error": f"'{obj}' debe ser un objeto (dict)"}
        internas = [k for k in claves if k not in empleado[obj]]
        if internas:
            return {"ok": False, "error": f"Faltan claves en '{obj}': {internas}"}

    return {"ok": True, "valor": empleado}
