import re

PATRON_RFC = r"^[A-Z]{4}\d{6}[A-Z0-9]{3}$"

#Agente 2 valida rfc
def agente_rfc_formato(empleado):
    rfc = empleado["rfc"]
    if re.match(PATRON_RFC, rfc):
        return {"ok": True, "valor": empleado}
    return {"ok": False, "error": f"RFC con formato inválido: '{rfc}'"}
