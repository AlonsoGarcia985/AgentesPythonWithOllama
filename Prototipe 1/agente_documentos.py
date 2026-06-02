from DatosMOCK import DOCUMENTOS_REQUERIDOS

#Agente revisa los documentos que esten en true
def agente_documentos(empleado):
    docs = empleado["documentos"]

    # acumulamos los faltantes: ausentes o con valor distinto de True
    faltantes = [d for d in DOCUMENTOS_REQUERIDOS if not docs.get(d, False)]

    if faltantes:
        advertencias = [f"Falta: {d}" for d in faltantes]
        return {"ok": True, "valor": empleado, "advertencias": advertencias}

    return {"ok": True, "valor": empleado}
