from config import conectar


def agente_departamento_bd(empleado):
    dep_id = empleado["departamento"]["id"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, activo FROM departamentos WHERE id = ?",
        (dep_id,),
    )
    fila = cursor.fetchone()
    conn.close()

    if fila is None:
        return {"ok": False, "error": f"Departamento con id {dep_id} no existe"}

    nombre_oficial, activo = fila
    if activo != 1:
        return {"ok": False, "error": f"Departamento '{nombre_oficial}' está inactivo"}


    empleado["departamento"]["nombre"] = nombre_oficial
    empleado["departamento"]["validado"] = True
    return {"ok": True, "valor": empleado}
