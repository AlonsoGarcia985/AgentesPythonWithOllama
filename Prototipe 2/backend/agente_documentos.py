from config import DOCUMENTOS_REQUERIDOS


def agente_documentos(empleado):
    docs = empleado["documentos"]
    faltantes = [d for d in DOCUMENTOS_REQUERIDOS if not docs.get(d, False)]
    if faltantes:
        advertencias = [f"Falta: {d}" for d in faltantes]
        return {"ok": True, "valor": empleado, "advertencias": advertencias}
    return {"ok": True, "valor": empleado}
