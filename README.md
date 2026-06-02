# Validador de Onboarding con Agentes + Ollama

Prototipo de consola que valida la información de un nuevo empleado mediante un **pipeline de agentes** y, al final, genera un **borrador de contrato laboral en español** usando un modelo de lenguaje local con **Ollama**. No usa base de datos ni interfaz gráfica: todo corre en la terminal y muestra el resultado de cada agente paso a paso.

## Descripción general

El sistema recibe un JSON con los datos de un empleado (con objetos anidados: departamento, puesto y documentos) y lo hace pasar por 7 agentes. Cada agente tiene **una sola responsabilidad**: valida o enriquece la información. Los primeros 6 agentes son Python puro (validaciones rápidas y deterministas); el séptimo llama a Ollama para redactar el contrato en lenguaje natural.

La idea central es la distinción entre dos resultados posibles de un agente:

- **Error fatal** (`ok: False`): detiene el pipeline. Los agentes siguientes no se ejecutan.
- **Advertencia** (`ok: True` + lista de advertencias): se registra la nota pero el pipeline continúa.

## Requisitos previos

- Python 3.9 o superior.
- [Ollama](https://ollama.com) instalado y corriendo localmente (expone una API en `localhost:11434`).
- El modelo descargado: `ollama pull llama3.2`.

La librería cliente de Python (`ollama`) se instala desde `requirements.txt` en el paso de instalación.

## Estructura del proyecto

```
onboarding/
├── main.py                   # punto de entrada: arma la lista de agentes y corre el pipeline
├── DatosMock.py             # datos simulados (la "base de datos" en memoria)
├── pipeline.py               # el orquestador + utilidades de color en consola
├── requirements.txt          # dependencias de Python
├── agente_claves.py          # AGENTE 1
├── agente_rfc_formato.py     # AGENTE 2
├── agente_rfc_duplicado.py   # AGENTE 3
├── agente_departamento.py    # AGENTE 4
├── agente_salario.py         # AGENTE 5
├── agente_documentos.py      # AGENTE 6
└── agente_contrato_ollama.py        # AGENTE 7 (usa Ollama)
```

## Instalación y ejecución

1. Entra a la carpeta del prototipo:

   ```bash
   cd "Prototipo 1"
   ```

2. Instala las dependencias de Python:

   ```bash
   pip install -r requirements.txt
   ```

3. Asegúrate de que Ollama esté corriendo y el modelo descargado (`ollama pull llama3.2`), y corre el pipeline:

   ```bash
   python main.py
   ```

Los agentes 1 a 6 responden casi al instante. El agente 7 tarda unos segundos (10–60s según el equipo), porque el modelo está generando el texto del contrato. Al final se imprime el contrato en español.

## Cómo funciona el pipeline

Todos los agentes comparten la **misma firma**: reciben el diccionario `empleado` y devuelven un diccionario con esta forma:

```python
{"ok": True/False, "valor": <empleado>, "error": <str>, "advertencias": [<str>, ...]}
```

El **orquestador** (`ejecutar_pipeline` en `pipeline.py`) no valida nada por sí mismo: solo coordina. Recorre la lista de agentes en orden y, según el resultado de cada uno:

- Si `ok` es `False` → imprime `✗`, muestra el error fatal y **detiene** el pipeline.
- Si `ok` es `True` con `advertencias` → imprime `⚠`, guarda la nota y **continúa**.
- Si `ok` es `True` sin notas → imprime `✓` y pasa el empleado (posiblemente enriquecido) al siguiente agente con `empleado = resultado["valor"]`.

El **orden importa**: cada agente confía en el trabajo del anterior. Por ejemplo, el agente 3 (RFC duplicado) solo se ejecuta si el agente 2 ya garantizó que el RFC tiene un formato válido.

## Qué hace cada agente

| # | Agente | Responsabilidad | Si falla |
|---|--------|-----------------|----------|
| 1 | `agente_claves` | Verifica que existan las 6 claves raíz y las claves internas de los objetos anidados. | Fatal |
| 2 | `agente_rfc_formato` | Valida el formato del RFC con regex: 4 letras + 6 dígitos + 3 alfanuméricos. | Fatal |
| 3 | `agente_rfc_duplicado` | Verifica que el RFC no esté ya registrado en `RFCS_REGISTRADOS`. | Fatal |
| 4 | `agente_departamento` | Confirma que el departamento exista y **enriquece** el empleado agregando `validado: True`. | Fatal |
| 5 | `agente_salario` | Verifica que el salario caiga dentro del rango permitido para el nivel del puesto. | Fatal |
| 6 | `agente_documentos` | Revisa que los documentos requeridos estén completos. Si faltan, genera advertencias. | Advertencia |
| 7 | `agente_contrato` | Llama a Ollama para generar el borrador de contrato y lo agrega al empleado en la clave `contrato`. | Fatal (si Ollama no responde) |

Los agentes 4 y 7 no solo validan: **enriquecen** el JSON. El agente 4 marca el departamento como validado y el agente 7 agrega el texto del contrato. Esos campos nuevos viajan por el resto del pipeline.

## Uso de Ollama

Las validaciones (agentes 1–6) son reglas exactas y se resuelven con Python puro: comparaciones, expresiones regulares y búsquedas en listas. No requieren inteligencia artificial.

El agente 7 es distinto: necesita **redactar** un contrato laboral en español formal, algo que no se puede lograr con `if/else`. Para eso se usa un modelo de lenguaje. **Ollama** es el programa que corre ese modelo (`llama3.2`) de forma local, sin enviar datos a internet ni requerir una API de paga. El flujo del agente 7 es:

1. Arma un *prompt* con los datos ya validados del empleado.
2. Lo envía al modelo con `ollama.chat(model="llama3.2", messages=[...])`.
3. Recibe el texto generado en `respuesta["message"]["content"]`.
4. Lo agrega al empleado en la clave `contrato`.

El agente incluye un manejo de errores: si Ollama no está corriendo, devuelve un error fatal con un mensaje claro en lugar de una excepción.

## Escenarios de prueba y resultados

Se probaron los cuatro escenarios solicitados:

**1. Caso exitoso.** Empleado válido (`Ana Torres`). Los 7 agentes se ejecutan. El agente 6 marca una advertencia porque falta `comprobante_domicilio`, pero el pipeline no se detiene y el contrato se genera.

```
✓ [1] agente_claves
✓ [2] agente_rfc_formato
✓ [3] agente_rfc_duplicado
✓ [4] agente_departamento
✓ [5] agente_salario
⚠ [6] agente_documentos
    ADVERTENCIA: Falta: comprobante_domicilio
✓ [7] agente_contrato
► Pipeline completado: 7/7 agentes ejecutados.
```

**2. RFC duplicado.** Se usó un RFC que ya está en `RFCS_REGISTRADOS`. El pipeline se detiene en el agente 3.

```
✓ [1] agente_claves
✓ [2] agente_rfc_formato
✗ [3] agente_rfc_duplicado
    ERROR FATAL: RFC ya registrado en el sistema: 'GOME850101AB1'
► Pipeline detenido. Los agentes siguientes no se ejecutaron.
```

**3. Salario fuera de rango.** Se asignó un salario de 50,000 a un puesto nivel `senior` (rango 22,000–40,000). El pipeline se detiene en el agente 5.

```
✓ [4] agente_departamento
✗ [5] agente_salario
    ERROR FATAL: Salario fuera del rango para senior ($22,000–$40,000)
► Pipeline detenido. Los agentes siguientes no se ejecutaron.
```

**4. Documentos incompletos.** Faltan documentos requeridos. A diferencia de los anteriores, este caso **no detiene** el pipeline: se registra la advertencia y el flujo continúa hasta generar el contrato.

```
⚠ [6] agente_documentos
    ADVERTENCIA: Falta: comprobante_domicilio
► Pipeline completado: 7/7 agentes ejecutados.
  Advertencias: ['Falta: comprobante_domicilio']
```

### Conclusión

El prototipo demuestra el patrón de pipeline de agentes con responsabilidades separadas, la diferencia entre errores fatales y advertencias, el enriquecimiento progresivo del JSON, y la combinación de validación determinista (Python) con generación de lenguaje natural (Ollama).
