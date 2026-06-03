from config import conectar


def agente_salario_bd(empleado):
    nivel = empleado["puesto"]["nivel"]
    salario = empleado["puesto"]["salario_base"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT salario_min, salario_max FROM puestos_rangos WHERE nivel = ?",
        (nivel,),
    )
    fila = cursor.fetchone()
    conn.close()

    if fila is None:
        return {"ok": False, "error": f"Nivel de puesto desconocido: '{nivel}'"}

    salario_min, salario_max = fila
    if not (salario_min <= salario <= salario_max):
        return {
            "ok": False,
            "error": (f"Salario fuera del rango para {nivel} "
                      f"(${salario_min:,.0f}–${salario_max:,.0f})"),
        }
    return {"ok": True, "valor": empleado}
