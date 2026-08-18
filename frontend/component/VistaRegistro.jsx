import { useState } from 'react';

export default function VistaEntrega() {
  const [criterioBusqueda, setCriterioBusqueda] = useState('');
  const [resultados, setResultados] = useState([]);
  const [vehiculoSeleccionado, setVehiculoSeleccionado] = useState(null);
  const [buscando, setBuscando] = useState(false);
  const [guardando, setGuardando] = useState(false);
  const [mensaje, setMensaje] = useState({ tipo: '', texto: '' });

  // Estado con los datos de la entrega
  const [datosSalida, setDatosSalida] = useState({
    oficio: '',
    nombre_recibe: '',
    ci_recibe: '',
    fecha_entrega: new Date().toLocaleDateString('es-ES'),
    observaciones: ''
  });

  // 1. Búsqueda por similitud
  const handleBuscar = async (e) => {
  e.preventDefault();
  if (!criterioBusqueda.trim()) return;

  setBuscando(true);
  setMensaje({ tipo: '', texto: '' });
  setResultados([]);
  setVehiculoSeleccionado(null);

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/v1/vehiculos/buscar?criterio=${encodeURIComponent(criterioBusqueda.trim())}`
    );
    const data = await response.json();

    if (response.ok && Array.isArray(data)) {
      if (data.length === 0) {
        setMensaje({ tipo: 'error', texto: 'No se encontraron vehículos coincidentes.' });
      } else {
        setResultados(data);
        if (data.length === 1) setVehiculoSeleccionado(data[0]);
      }
    } else {
      const msgError = typeof data === 'string' ? data : (data.detail || 'No se encontraron datos.');
      setMensaje({ tipo: 'error', texto: msgError });
    }
  } catch {
    setMensaje({ tipo: 'error', texto: 'Error de conexión con el servidor backend Python (FastAPI).' });
  } finally {
    setBuscando(false);
  }
};

  const handleChangeSalida = (e) => {
    const { name, value } = e.target;
    setDatosSalida((prev) => ({ ...prev, [name]: value }));
  };

  // 2. Procesar la entrega del vehículo seleccionado
  const handleConfirmarEntrega = async (e) => {
    e.preventDefault();
    if (!datosSalida.oficio || !datosSalida.nombre_recibe || !datosSalida.ci_recibe) {
      setMensaje({ tipo: 'error', texto: 'Por favor complete N° de Oficio, Nombre y Cédula de quien retira.' });
      return;
    }

    setGuardando(true);
    setMensaje({ tipo: '', texto: '' });

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/vehiculos/${vehiculoSeleccionado.id}/entrega`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datosSalida)
      });

      const data = await response.json();

      if (response.ok) {
        setMensaje({ tipo: 'exito', texto: `¡Salida procesada con éxito! El vehículo Acta #${vehiculoSeleccionado.id} pasó a estado ENTREGADO.` });
        setVehiculoSeleccionado(null);
        setResultados([]);
        setCriterioBusqueda('');
        setDatosSalida({
          oficio: '',
          nombre_recibe: '',
          ci_recibe: '',
          fecha_entrega: new Date().toLocaleDateString('es-ES'),
          observaciones: ''
        });
      } else {
        setMensaje({ tipo: 'error', texto: data.detail || 'Ocurrió un error al procesar la entrega.' });
      }
    } catch {
      setMensaje({ tipo: 'error', texto: 'Error de comunicación con el backend al intentar registrar la salida.' });
    } finally {
      setGuardando(false);
    }
  };

  return (
    <div style={containerStyle}>
      {/* Encabezado */}
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.6rem', color: '#0f172a', margin: 0 }}>
          🚚 MÓDULO DE SALIDA Y ENTREGA DE VEHÍCULOS
        </h2>
        <p style={{ color: '#64748b', fontSize: '0.9rem', marginTop: '0.3rem' }}>
          Búsqueda por similitud (Matrícula / Chasis) y orden de liberación
        </p>
      </div>

      {/* Alertas */}
      {mensaje.texto && (
        <div style={{
          padding: '0.8rem 1rem',
          borderRadius: '6px',
          marginBottom: '1.2rem',
          fontWeight: '500',
          fontSize: '0.9rem',
          backgroundColor: mensaje.tipo === 'exito' ? '#dcfce7' : '#fee2e2',
          color: mensaje.tipo === 'exito' ? '#166534' : '#991b1b',
          border: `1px solid ${mensaje.tipo === 'exito' ? '#86efac' : '#fca5a5'}`
        }}>
          {mensaje.texto}
        </div>
      )}

      {/* Buscador */}
      <form onSubmit={handleBuscar} style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        <input
          type="text"
          value={criterioBusqueda}
          onChange={(e) => setCriterioBusqueda(e.target.value)}
          placeholder="Escriba parte de la Matrícula o Chasis (Ej: ABC, 123...)"
          style={inputStyle}
        />
        <button type="submit" disabled={buscando} style={btnBuscarStyle(buscando)}>
          {buscando ? '🔍 Buscando...' : '🔍 Buscar'}
        </button>
      </form>

      {/* LISTA DE COINCIDENCIAS (Cuando hay múltiples resultados) */}
      {resultados.length > 1 && !vehiculoSeleccionado && (
        <div style={{ marginBottom: '1.5rem' }}>
          <h4 style={{ color: '#0f172a', marginBottom: '0.5rem', fontSize: '0.95rem' }}>
            Coincidencias encontradas ({resultados.length}). Seleccione el rodado correspondiente:
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {resultados.map((v) => (
              <div
                key={v.id}
                onClick={() => setVehiculoSeleccionado(v)}
                style={itemCoincidenciaStyle}
              >
                <div>
                  <strong>Acta #{v.id}</strong> — {v.marca} {v.modelo}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#0284c7', fontWeight: 'bold' }}>
                  Chapa: {v.matricula || v.Matricula || 'S/N'} | Chasis: {v.chasis || 'S/N'} ➔
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* FICHA Y FORMULARIO DEL VEHÍCULO SELECCIONADO */}
      {vehiculoSeleccionado && (
        <div style={fichaStyle}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0, color: '#0f172a', fontSize: '1.1rem' }}>
              📋 Rodado Seleccionado para Devolución
            </h3>
            {resultados.length > 1 && (
              <button
                type="button"
                onClick={() => setVehiculoSeleccionado(null)}
                style={{ backgroundColor: 'transparent', border: 'none', color: '#0284c7', cursor: 'pointer', fontWeight: 'bold' }}
              >
                ↩ Elegir otro de la lista
              </button>
            )}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.8rem', fontSize: '0.88rem', color: '#334155', backgroundColor: '#ffffff', padding: '1rem', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
            <div><strong>N° de Acta / ID:</strong> #{vehiculoSeleccionado.id}</div>
            <div><strong>Estado:</strong> <span style={{ color: '#d97706', fontWeight: 'bold' }}>{vehiculoSeleccionado.estado}</span></div>
            <div><strong>Marca / Modelo:</strong> {vehiculoSeleccionado.marca} {vehiculoSeleccionado.modelo}</div>
            <div><strong>Matrícula / Chapa:</strong> {vehiculoSeleccionado.matricula || vehiculoSeleccionado.Matricula || 'S/N'}</div>
            <div><strong>N° Chasis:</strong> {vehiculoSeleccionado.chasis || 'S/N'}</div>
            <div><strong>Tipo:</strong> {vehiculoSeleccionado.tipo}</div>
          </div>

          <hr style={{ border: 'none', borderTop: '1px solid #e2e8f0', margin: '1.5rem 0' }} />

          <h4 style={{ color: '#0f172a', margin: '0 0 1rem 0', fontSize: '1rem' }}>
            📝 Datos de la Orden de Salida / Liberación
          </h4>

          <form onSubmit={handleConfirmarEntrega} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <label style={labelStyle}>N° de Oficio Judicial *</label>
                <input
                  type="text"
                  name="oficio"
                  value={datosSalida.oficio}
                  onChange={handleChangeSalida}
                  placeholder="Ej: Oficio N° 458/2026"
                  style={inputStyle}
                  required
                />
              </div>

              <div>
                <label style={labelStyle}>Fecha de Salida</label>
                <input
                  type="text"
                  name="fecha_entrega"
                  value={datosSalida.fecha_entrega}
                  onChange={handleChangeSalida}
                  style={inputStyle}
                />
              </div>

              <div>
                <label style={labelStyle}>Nombre de quien Retira *</label>
                <input
                  type="text"
                  name="nombre_recibe"
                  value={datosSalida.nombre_recibe}
                  onChange={handleChangeSalida}
                  placeholder="Nombre y apellido completo"
                  style={inputStyle}
                  required
                />
              </div>

              <div>
                <label style={labelStyle}>Cédula de Identidad N° *</label>
                <input
                  type="text"
                  name="ci_recibe"
                  value={datosSalida.ci_recibe}
                  onChange={handleChangeSalida}
                  placeholder="N° Documento del receptor"
                  style={inputStyle}
                  required
                />
              </div>
            </div>

            <div>
              <label style={labelStyle}>Observaciones de Entrega</label>
              <textarea
                name="observaciones"
                value={datosSalida.observaciones}
                onChange={handleChangeSalida}
                placeholder="Detalles adicionales..."
                style={{ ...inputStyle, height: '70px', resize: 'vertical' }}
              />
            </div>

            <button type="submit" disabled={guardando} style={btnConfirmarStyle(guardando)}>
              {guardando ? '⌛ Procesando Salida...' : '✅ Confirmar Liberación y Salida del Sistema'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

// Estilos integrados
const containerStyle = { maxWidth: '820px', margin: '0 auto', backgroundColor: '#ffffff', padding: '2.5rem', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.08)', border: '1px solid #e2e8f0' };
const labelStyle = { display: 'block', fontWeight: 'bold', fontSize: '0.82rem', color: '#334155', marginBottom: '0.35rem', textTransform: 'uppercase', letterSpacing: '0.5px' };
const inputStyle = { width: '100%', padding: '0.65rem 0.8rem', border: '1px solid #cbd5e1', borderRadius: '6px', fontSize: '0.9rem', boxSizing: 'border-box', outline: 'none', backgroundColor: '#f8fafc', color: '#0f172a' };
const fichaStyle = { backgroundColor: '#f8fafc', padding: '1.5rem', borderRadius: '8px', border: '1px solid #cbd5e1' };
const btnBuscarStyle = (cargando) => ({ padding: '0.65rem 1.2rem', backgroundColor: cargando ? '#94a3b8' : '#0284c7', color: '#ffffff', border: 'none', borderRadius: '6px', cursor: cargando ? 'not-allowed' : 'pointer', fontWeight: 'bold', fontSize: '0.9rem' });
const btnConfirmarStyle = (cargando) => ({ width: '100%', marginTop: '0.5rem', padding: '0.75rem', backgroundColor: cargando ? '#94a3b8' : '#16a34a', color: '#ffffff', border: 'none', borderRadius: '6px', cursor: cargando ? 'not-allowed' : 'pointer', fontWeight: 'bold', fontSize: '0.95rem' });
const itemCoincidenciaStyle = { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 1rem', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '6px', cursor: 'pointer', transition: 'background-color 0.2s' };