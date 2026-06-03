import re

from config import PATRON_RFC


def agente_rfc_formato(empleado):
    rfc = empleado["rfc"]
    if re.match(PATRON_RFC, rfc):
        return {"ok": True, "valor": empleado}
    return {"ok": False, "error": f"RFC con formato inválido: '{rfc}'"}
