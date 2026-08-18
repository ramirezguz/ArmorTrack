import { useState } from 'react';

export default function VistaEntrega() {
  // --- ESTADOS ---
  const [criterioBusqueda, setCriterioBusqueda] = useState('');
  const [buscando, setBuscando] = useState(false);
  const [resultados, setResultados] = useState([]);
  const [vehiculoSeleccionado, setVehiculoSeleccionado] = useState(null);
  
  const [mensaje, setMensaje] = useState({ tipo: '', texto: '' });
  const [enviando, setEnviando] = useState(false);

  // Estado para el formulario de salida (persona que recibe y oficial que entrega)
  const [datosSalida, setDatosSalida] = useState({
    fecha_entrega: new Date().toISOString().split('T')[0], // Fecha actual por defecto
    
    // Datos de la persona que retira
    nombre_recibe: '',
    documento_recibe: '',
    
    // Datos del Personal / Oficial de Guardia que entrega
    grado_entrega: '',
    nombre_entrega: '',
    
    // Observaciones u Oficio
    observaciones: ''
  });

  // --- MANEJADORES DE EVENTOS ---

  // 1. Manejar cambios en el formulario de entrega
  const handleChangeSalida = (e) => {
    const { name, value } = e.target;
    setDatosSalida((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  // 2. Buscar vehículo retenido
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
          setMensaje({
            tipo: 'error',
            texto: 'No se encontraron vehículos que coincidan con la búsqueda.'
          });
        } else {
          setResultados(data);
          if (data.length === 1) {
            setVehiculoSeleccionado(data[0]);
          }
        }
      } else {
        setMensaje({
          tipo: 'error',
          texto: data.detail || 'Ocurrió un error al consultar los vehículos.'
        });
      }
    } catch (err) {
      console.error('Error en fetch:', err);
      setMensaje({
        tipo: 'error',
        texto: 'Error de comunicación con el servidor backend Python (FastAPI).'
      });
    } finally {
      setBuscando(false);
    }
  };

  // 3. Confirmar registro de salida / entrega
  const handleRegistrarSalida = async (e) => {
    e.preventDefault();
    if (!vehiculoSeleccionado) {
      setMensaje({ tipo: 'error', texto: 'Por favor, selecciona un vehículo primero.' });
      return;
    }

    setEnviando(true);
    setMensaje({ tipo: '', texto: '' });

    try {
      const payload = {
        vehiculo_id: vehiculoSeleccionado.id,
        ...datosSalida
      };

      const response = await fetch('http://127.0.0.1:8000/api/v1/vehiculos/salida', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok) {
        setMensaje({ tipo: 'exito', texto: '¡Salida del vehículo registrada con éxito!' });
        setVehiculoSeleccionado(null);
        setResultados([]);
        setCriterioBusqueda('');
        setDatosSalida({
          fecha_entrega: new Date().toISOString().split('T')[0],
          nombre_recibe: '',
          documento_recibe: '',
          grado_entrega: '',
          nombre_entrega: '',
          observaciones: ''
        });
      } else {
        setMensaje({ tipo: 'error', texto: data.detail || 'Error al registrar la salida.' });
      }
    } catch (err) {
      console.error('Error al registrar salida:', err);
      setMensaje({ tipo: 'error', texto: 'Error al conectar con el servidor.' });
    } finally {
      setEnviando(false);
    }
  };

  // --- ESTILOS EN LÍNEA ---
  const containerStyle = { padding: '20px', maxWidth: '800px', margin: '0 auto', fontFamily: 'sans-serif' };
  const cardStyle = { backgroundColor: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '20px', marginBottom: '20px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' };
  const labelStyle = { display: 'block', fontWeight: 'bold', marginBottom: '5px', fontSize: '14px', color: '#4a5568' };
  const inputStyle = { width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e0', marginBottom: '15px', fontSize: '14px', boxSizing: 'border-box' };
  const buttonStyle = { backgroundColor: '#0284c7', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' };
  const sectionHeaderStyle = { fontSize: '15px', fontWeight: 'bold', color: '#1e293b', marginBottom: '12px', borderBottom: '1px solid #cbd5e0', paddingBottom: '5px' };

  return (
    <div style={containerStyle}>
      <div style={{ textAlign: 'center', marginBottom: '25px' }}>
        <h2>🚚 MÓDULO DE SALIDA Y ENTREGA DE VEHÍCULOS</h2>
        <p style={{ color: '#64748b' }}>Registro de devolución y liberación de rodados por oficio judicial</p>
      </div>

      {/* ALERTAS Y MENSAJES */}
      {mensaje.texto && (
        <div style={{
          padding: '12px 16px',
          borderRadius: '6px',
          marginBottom: '20px',
          backgroundColor: mensaje.tipo === 'error' ? '#fee2e2' : '#dcfce7',
          color: mensaje.tipo === 'error' ? '#991b1b' : '#166534',
          border: `1px solid ${mensaje.tipo === 'error' ? '#f87171' : '#4ade80'}`
        }}>
          {mensaje.texto}
        </div>
      )}

      {/* FORMULARIO DE BÚSQUEDA */}
      <div style={cardStyle}>
        <form onSubmit={handleBuscar} style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            placeholder="Ingrese matrícula o número de chasis..."
            value={criterioBusqueda}
            onChange={(e) => setCriterioBusqueda(e.target.value)}
            style={{ ...inputStyle, marginBottom: 0 }}
          />
          <button type="submit" style={buttonStyle} disabled={buscando}>
            {buscando ? 'Buscando...' : '🔍 Buscar'}
          </button>
        </form>
      </div>

      {/* SELECCIÓN DE RESULTADOS (SI HAY MÁS DE UNO) */}
      {resultados.length > 1 && !vehiculoSeleccionado && (
        <div style={cardStyle}>
          <h3>Selecciona el vehículo correspondiente:</h3>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {resultados.map((v) => (
              <li
                key={v.id}
                onClick={() => setVehiculoSeleccionado(v)}
                style={{
                  padding: '12px',
                  border: '1px solid #e2e8f0',
                  borderRadius: '6px',
                  marginBottom: '8px',
                  cursor: 'pointer',
                  backgroundColor: '#f8fafc'
                }}
              >
                <strong>{v.tipo} {v.marca} {v.modelo}</strong> — Chapa: {v.matricula || 'S/N'} | Chasis: {v.chasis || 'S/N'}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* FORMULARIO DE REGISTRO DE SALIDA */}
      {vehiculoSeleccionado && (
        <div style={cardStyle}>
          <h3 style={{ marginTop: 0, color: '#1e293b' }}>
            Vehículo Seleccionado: {vehiculoSeleccionado.marca} {vehiculoSeleccionado.modelo} ({vehiculoSeleccionado.matricula})
          </h3>
          <hr style={{ border: 'none', borderTop: '1px solid #e2e8f0', margin: '15px 0' }} />

          <form onSubmit={handleRegistrarSalida}>
            
            {/* SECCIÓN 1: DATOS GENERALES */}
            <div>
              <label style={labelStyle}>Fecha de Salida</label>
              <input
                type="date"
                name="fecha_entrega"
                value={datosSalida.fecha_entrega}
                onChange={handleChangeSalida}
                style={inputStyle}
                required
              />
            </div>

            {/* SECCIÓN 2: DATOS DE QUIEN RETIRA */}
            <div style={sectionHeaderStyle}>👤 Datos de la Persona que Retira</div>

            <div>
              <label style={labelStyle}>Nombre y Apellido Completo *</label>
              <input
                type="text"
                name="nombre_recibe"
                value={datosSalida.nombre_recibe}
                onChange={handleChangeSalida}
                placeholder="Ej: Juan Pérez"
                style={inputStyle}
                required
              />
            </div>

            <div>
              <label style={labelStyle}>Documento / C.I. *</label>
              <input
                type="text"
                name="documento_recibe"
                value={datosSalida.documento_recibe}
                onChange={handleChangeSalida}
                placeholder="Ej: 1.234.567"
                style={inputStyle}
                required
              />
            </div>

            {/* SECCIÓN 3: DATOS DEL OFICIAL DE GUARDIA QUE ENTREGA */}
            <div style={{ ...sectionHeaderStyle, marginTop: '10px' }}>👮‍♂️ Datos del Oficial / Personal de Guardia que Entrega</div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '10px' }}>
              <div>
                <label style={labelStyle}>Grado / Jerarquía *</label>
                <input
                  type="text"
                  name="grado_entrega"
                  value={datosSalida.grado_entrega}
                  onChange={handleChangeSalida}
                  placeholder="Ej: Oficial Insp. / Subof."
                  style={inputStyle}
                  required
                />
              </div>

              <div>
                <label style={labelStyle}>Nombre y Apellido del Oficial *</label>
                <input
                  type="text"
                  name="nombre_entrega"
                  value={datosSalida.nombre_entrega}
                  onChange={handleChangeSalida}
                  placeholder="Nombre y Apellido del intervenciente"
                  style={inputStyle}
                  required
                />
              </div>
            </div>


            {/* SECCIÓN 4: OBSERVACIONES */}
            <div style={{ ...sectionHeaderStyle, marginTop: '10px' }}>📋 Detalles Finales</div>

            <div>
              <label style={labelStyle}>Observaciones / Nro. Oficio Judicial</label>
              <textarea
                name="observaciones"
                rows="3"
                value={datosSalida.observaciones}
                onChange={handleChangeSalida}
                placeholder="Detalles del Oficio, oficio judicial, etc."
                style={{ ...inputStyle, fontFamily: 'inherit' }}
              />
            </div>

            <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
              <button type="submit" style={buttonStyle} disabled={enviando}>
                {enviando ? 'Procesando...' : '✅ Confirmar Entrega'}
              </button>
              <button
                type="button"
                onClick={() => setVehiculoSeleccionado(null)}
                style={{ ...buttonStyle, backgroundColor: '#64748b' }}
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}