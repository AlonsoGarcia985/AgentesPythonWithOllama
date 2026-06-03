from config import conectar


def agente_rfc_bd(empleado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM empleados WHERE rfc = ?",
        (empleado["rfc"],),
    )
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return {"ok": False, "error": f"RFC {empleado['rfc']} ya registrado en la BD"}
    return {"ok": True, "valor": empleado}
