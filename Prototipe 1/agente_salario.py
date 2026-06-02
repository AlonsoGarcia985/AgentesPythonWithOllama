from DatosMOCK import RANGOS_SALARIALES

#Agente 5 salario, verifica el rango
def agente_salario(empleado):
    nivel = empleado["puesto"]["nivel"]
    salario = empleado["puesto"]["salario_base"]

    # el nivel debe existir en la tabla de rangos
    if nivel not in RANGOS_SALARIALES:
        return {"ok": False, "error": f"Nivel de puesto desconocido: '{nivel}'"}

    rango = RANGOS_SALARIALES[nivel]

    # ¿el salario cae dentro de [min, max]?
    if not (rango["min"] <= salario <= rango["max"]):
        return {
            "ok": False,
            "error": (f"Salario fuera del rango para {nivel} "
                      f"(${rango['min']:,}–${rango['max']:,})"),
        }

    return {"ok": True, "valor": empleado}
