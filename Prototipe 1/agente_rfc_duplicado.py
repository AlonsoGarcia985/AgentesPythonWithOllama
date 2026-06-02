from DatosMOCK import RFCS_REGISTRADOS


# agente 3, rfc duplicados

def agente_rfc_duplicado(empleado):
    rfc = empleado["rfc"]
    if rfc in RFCS_REGISTRADOS:
        return {"ok": False, "error": f"RFC ya registrado en el sistema: '{rfc}'"}
    return {"ok": True, "valor": empleado}

