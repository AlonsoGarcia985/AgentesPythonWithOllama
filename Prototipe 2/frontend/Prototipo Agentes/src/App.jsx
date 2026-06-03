import { useState } from 'react'

// JSON de ejemplo precargado en el textarea (puedes editarlo en pantalla)
const EMPLEADO_DEMO = {
  nombre: "Ana Torres",
  rfc: "TORA900315AB2",
  departamento: { id: 3, nombre: "Ingeniería" },
  puesto: { titulo: "Desarrollador Sr", nivel: "senior", salario_base: 28000 },
  documentos: { ine: true, curp: true, comprobante_domicilio: false, acta_nacimiento: true },
  fecha_inicio: "2024-09-01",
}

const API_URL = "http://localhost:8000/validar-empleado"

function App() {
  const [texto, setTexto] = useState(JSON.stringify(EMPLEADO_DEMO, null, 2))
  const [resultado, setResultado] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  async function validar() {
    setError(null)
    setResultado(null)

    // 1) Parsear el JSON del textarea
    let empleado
    try {
      empleado = JSON.parse(texto)
    } catch (e) {
      setError("El JSON no es válido: " + e.message)
      return
    }

    // 2) Llamar a la API (fetch POST)
    setCargando(true)
    try {
      const resp = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(empleado),
      })
      const data = await resp.json()
      setResultado(data)
    } catch (e) {
      setError("No se pudo conectar con el servidor (¿está corriendo en :8000?): " + e.message)
    } finally {
      setCargando(false)
    }
  }

  // Decide el ícono y color de cada agente según su estado
  const icono = (a) => (!a.ok ? "✗" : a.advertencias ? "⚠" : "✓")
  const color = (a) => (!a.ok ? "#c0392b" : a.advertencias ? "#b8860b" : "#27ae60")

  const cajaTexto = {
    whiteSpace: "pre-wrap", background: "#f5f5f5",
    padding: 16, borderRadius: 6, lineHeight: 1.5,
  }

  return (
    <div style={{ maxWidth: 820, margin: "2rem auto", padding: "0 1rem",
                  fontFamily: "system-ui, sans-serif" }}>
      <h1>Validador de Onboarding</h1>
      <p>Pega o edita el JSON del empleado y pulsa <strong>Validar</strong>.</p>

      <textarea
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        rows={16}
        style={{ width: "100%", fontFamily: "monospace", fontSize: 13,
                 padding: 10, boxSizing: "border-box" }}
      />

      <button
        onClick={validar}
        disabled={cargando}
        style={{ marginTop: 10, padding: "10px 22px", fontSize: 16,
                 cursor: cargando ? "default" : "pointer" }}
      >
        {cargando ? "Validando..." : "Validar"}
      </button>

      {error && <p style={{ color: "#c0392b", marginTop: 16 }}>{error}</p>}

      {resultado && (
        <div style={{ marginTop: 24 }}>
          <h2>Resultado: {resultado.ok ? "✅ Aprobado" : "❌ Detenido"}</h2>

          <ul style={{ listStyle: "none", padding: 0 }}>
            {resultado.agentes.map((a, i) => (
              <li key={i} style={{ color: color(a), padding: "4px 0",
                                   fontFamily: "monospace" }}>
                {icono(a)} {a.nombre}
                {a.error && <span> — {a.error}</span>}
                {a.advertencias && <span> — {a.advertencias.join(", ")}</span>}
              </li>
            ))}
          </ul>

          {resultado.empleado?.contrato && (
            <>
              <h3>📄 Contrato</h3>
              <pre style={cajaTexto}>{resultado.empleado.contrato}</pre>
            </>
          )}

          {resultado.empleado?.correo && (
            <>
              <h3>✉️ Correo de bienvenida</h3>
              <pre style={cajaTexto}>{resultado.empleado.correo}</pre>
            </>
          )}
        </div>
      )}
    </div>
  )
}

export default App
