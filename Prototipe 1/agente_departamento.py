from DatosMOCK import DEPARTAMENTOS_VALIDOS

#Agente 4 Busca por ID  
def agente_departamento(empleado):
    dep_id = empleado["departamento"]["id"]

    # lista de ids válidos a partir de los datos mock
    ids_validos = [d["id"] for d in DEPARTAMENTOS_VALIDOS]

    if dep_id not in ids_validos:
        return {"ok": False, "error": f"Departamento con id {dep_id} no es válido"}

    # ── enriquecimiento: marcamos el departamento como validado ──
    empleado["departamento"]["validado"] = True

    return {"ok": True, "valor": empleado}
