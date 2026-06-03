def ejecutar_pipeline(empleado, agentes):
    resultados = []

    for agente in agentes:
        nombre = agente.__name__
        r = agente(empleado)


        if not r.get("ok"):
            resultados.append({"nombre": nombre, "ok": False, "error": r.get("error")})
            return {"ok": False, "agentes": resultados, "empleado": empleado}


        empleado = r["valor"]
        entrada = {"nombre": nombre, "ok": True}
        if r.get("advertencias"):
            entrada["advertencias"] = r["advertencias"]
        resultados.append(entrada)

    return {"ok": True, "agentes": resultados, "empleado": empleado}
