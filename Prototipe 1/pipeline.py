class C:
    OK = "\033[92m"  # verde
    WARN = "\033[93m"  # amarillo
    ERR = "\033[91m"  # rojo
    DIM = "\033[90m"  # gris
    BOLD = "\033[1m"
    RESET = "\033[0m"


#  ORQUESTADOR — corre la lista de agentes e imprime paso a paso

def ejecutar_pipeline(empleado, agentes):
    print(f"{C.DIM}Empleado: {empleado.get('nombre', '(sin nombre)')}{C.RESET}\n")

    advertencias_totales = []

    for i, agente in enumerate(agentes, start=1):
        nombre = agente.__name__
        resultado = agente(empleado)

        # ── caso FATAL: el agente falló ──
        if not resultado.get("ok"):
            print(f"{C.ERR}✗ [{i}] {nombre}{C.RESET}")
            print(f"    {C.ERR}ERROR FATAL: {resultado.get('error')}{C.RESET}")
            print(f"\n{C.ERR}{C.BOLD}► Pipeline detenido. "
                  f"Los agentes siguientes no se ejecutaron.{C.RESET}")
            return {
                "ok": False,
                "agente_fallido": nombre,
                "error": resultado.get("error"),
                "empleado": empleado,
            }

        # ── caso OK: actualizamos el empleado (puede venir enriquecido) ──
        empleado = resultado["valor"]

        # ── caso ADVERTENCIA: ok=True pero con notas ──
        advertencias = resultado.get("advertencias", [])
        if advertencias:
            advertencias_totales.extend(advertencias)
            print(f"{C.WARN}⚠ [{i}] {nombre}{C.RESET}")
            for adv in advertencias:
                print(f"    {C.WARN}ADVERTENCIA: {adv}{C.RESET}")
        else:
            print(f"{C.OK}✓ [{i}] {nombre}{C.RESET}")

    # ── resumen final ──
    print(f"\n{C.OK}{C.BOLD}► Pipeline completado: {len(agentes)}/{len(agentes)} "
          f"agentes ejecutados.{C.RESET}")
    if advertencias_totales:
        print(f"{C.WARN}  Advertencias: {advertencias_totales}{C.RESET}")

    return {
        "ok": True,
        "empleado": empleado,
        "advertencias": advertencias_totales,
    }