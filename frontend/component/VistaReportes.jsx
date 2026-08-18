import { useState, useEffect } from 'react';

export default function VistaReportes() {
  // -------------------------------------------------------------
  // 1. ESTADOS
  // -------------------------------------------------------------
  const [criterioBusqueda, setCriterioBusqueda] = useState('');
  const [estadoFiltro, setEstadoFiltro] = useState('TODOS'); // TODOS | INCAUTADO| DEPOSITADO | ENTREGADO
  const [reportes, setReportes] = useState([]);
  const [estadisticas, setEstadisticas] = useState({ total: 0, vehiculos: 0, motos: 0 });
  const [cargando, setCargando] = useState(false);
  const [tarjetasAbiertas, setTarjetasAbiertas] = useState({});

  // -------------------------------------------------------------
  // 2. EFECTO DE CARGA INICIAL
  // -------------------------------------------------------------
  useEffect(() => {
    let ignore = false;

    const cargarDatosIniciales = async () => {
      // Cargar Estadísticas
      try {
        const resStats = await fetch('http://127.0.0.1:8000/api/v1/estadisticas');
        if (resStats.ok && !ignore) {
          const dataStats = await resStats.json();
          setEstadisticas(dataStats);
        }
      } catch (err) {
        console.error('Error al cargar estadísticas:', err);
      }

      // Cargar Reportes Iniciales
      setCargando(true);
      try {
        const resReportes = await fetch('http://127.0.0.1:8000/api/v1/vehiculos/buscar?criterio=');
        if (resReportes.ok && !ignore) {
          const dataReportes = await resReportes.json();
          setReportes(Array.isArray(dataReportes) ? dataReportes : []);
        } else if (!ignore) {
          setReportes([]);
        }
      } catch (err) {
        console.error('Error al consultar reportes:', err);
        if (!ignore) setReportes([]);
      } finally {
        if (!ignore) setCargando(false);
      }
    };

    cargarDatosIniciales();

    return () => {
      ignore = true;
    };
  }, []);

  // -------------------------------------------------------------
  // 3. FUNCIONES DE BÚSQUEDA Y CONSULTA
  // -------------------------------------------------------------
  const cargarReportes = async (criterio = '', estado = estadoFiltro) => {
    setCargando(true);
    try {
      const queryParams = new URLSearchParams({
        criterio: criterio.trim(),
        estado: estado
      });

      const url = `http://127.0.0.1:8000/api/v1/vehiculos/buscar?${queryParams.toString()}`;

      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setReportes(Array.isArray(data) ? data : []);
      } else {
        setReportes([]);
      }
    } catch (err) {
      console.error('Error al consultar reportes:', err);
      setReportes([]);
    } finally {
      setCargando(false);
    }
  };

  const handleFiltrar = (e) => {
    if (e) e.preventDefault();
    cargarReportes(criterioBusqueda, estadoFiltro);
  };

  const handleCambioEstado = (e) => {
    const nuevoEstado = e.target.value;
    setEstadoFiltro(nuevoEstado);
    cargarReportes(criterioBusqueda, nuevoEstado);
  };

  const toggleTarjeta = (id) => {
    setTarjetasAbiertas((prev) => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  // -------------------------------------------------------------
  // 4. FILTRADO LOCAL
  // -------------------------------------------------------------
  const reportesFiltrados = reportes.filter((vehiculo) => {
    if (estadoFiltro === 'TODOS') return true;
    const est = (vehiculo.estado || '').toUpperCase();
    
    if (estadoFiltro === 'INCAUTADO') {
      return est === 'INCAUTADO' || est === 'INCAUTADO';
    }
    return est === estadoFiltro;
  });

  // -------------------------------------------------------------
  // 5. ESTILOS AUXILIARES
  // -------------------------------------------------------------
  const containerStyle = {
    padding: '20px',
    maxWidth: '1000px',
    margin: '0 auto',
    fontFamily: 'sans-serif'
  };

  const statCardStyle = {
    flex: 1,
    backgroundColor: '#1e293b',
    color: '#fff',
    borderRadius: '8px',
    padding: '15px 20px',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  };

  const cardStyle = {
    backgroundColor: '#18181b',
    border: '1px solid #27272a',
    borderRadius: '10px',
    marginBottom: '12px',
    overflow: 'hidden',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.2)',
    transition: 'all 0.2s ease-in-out'
  };

  const inputStyle = {
    padding: '12px 16px',
    borderRadius: '8px',
    border: '1px solid #3f3f46',
    backgroundColor: '#18181b',
    color: '#fff',
    fontSize: '14px',
    outline: 'none'
  };

  // -------------------------------------------------------------
  // 6. INTERFAZ Y RENDERIZADO
  // -------------------------------------------------------------
  return (
    <div style={containerStyle}>
      {/* TÍTULO PRINCIPAL */}
      <div style={{ textAlign: 'center', marginBottom: '20px' }}>
        <h2 style={{ color: '#f8fafc', margin: 0 }}>📊 PANEL DE REPORTES E INVENTARIO</h2>
        <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '5px' }}>
          Consolidado general de vehículos incautados y estado de depósito
        </p>
      </div>

      {/* TARJETAS DE ESTADÍSTICAS */}
      <div style={{ display: 'flex', gap: '15px', marginBottom: '20px' }}>
        <div style={statCardStyle}>
          <span style={{ fontSize: '24px' }}>📋</span>
          <div>
            <div style={{ fontSize: '12px', color: '#94a3b8', fontWeight: 'bold' }}>TOTAL REGISTROS</div>
            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#38bdf8' }}>{estadisticas.total || 0}</div>
          </div>
        </div>

        <div style={statCardStyle}>
          <span style={{ fontSize: '24px' }}>🚗</span>
          <div>
            <div style={{ fontSize: '12px', color: '#94a3b8', fontWeight: 'bold' }}>AUTOMOTORES</div>
            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#4ade80' }}>{estadisticas.vehiculos || 0}</div>
          </div>
        </div>

        <div style={statCardStyle}>
          <span style={{ fontSize: '24px' }}>🏍️</span>
          <div>
            <div style={{ fontSize: '12px', color: '#94a3b8', fontWeight: 'bold' }}>MOTOCICLETAS</div>
            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#fb923c' }}>{estadisticas.motos || 0}</div>
          </div>
        </div>
      </div>

      {/* BARRA DE BÚSQUEDA Y FILTROS DE ESTADO */}
      <form onSubmit={handleFiltrar} style={{ display: 'flex', gap: '10px', marginBottom: '25px', flexWrap: 'wrap' }}>
        {/* Campo de Texto */}
        <input
          type="text"
          placeholder="Buscar por Matrícula, Chasis, Marca, Conductor o Fiscalía..."
          value={criterioBusqueda}
          onChange={(e) => setCriterioBusqueda(e.target.value)}
          style={{ ...inputStyle, flex: 2, minWidth: '220px' }}
        />

        {/* Desplegable de Estados */}
        <select
          value={estadoFiltro}
          onChange={handleCambioEstado}
          style={{ ...inputStyle, flex: 1, minWidth: '180px', cursor: 'pointer' }}
        >
          <option value="TODOS">📌 Todos los Estados</option>
          <option value="INCAUTADO">🔴 Incautado</option>
          <option value="DEPOSITADO">📦 Depositado</option>
          <option value="ENTREGADO">🟢 Entregado</option>
        </select>

        {/* Botón Buscar */}
        <button
          type="submit"
          disabled={cargando}
          style={{
            backgroundColor: '#0284c7',
            color: 'white',
            padding: '12px 24px',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontWeight: 'bold',
            fontSize: '14px'
          }}
        >
          {cargando ? 'Filtrando...' : '🔍 Filtrar'}
        </button>
      </form>

      {/* LISTADO FILTRADO */}
      {reportesFiltrados.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#71717a', backgroundColor: '#18181b', borderRadius: '8px', border: '1px solid #27272a' }}>
          ⚠️ No hay registros con el estado <strong>"{estadoFiltro}"</strong> o con ese criterio de búsqueda.
        </div>
      ) : (
        reportesFiltrados.map((vehiculo) => {
          const idItem = vehiculo.id;
          const estaAbierto = !!tarjetasAbiertas[idItem];

          const tipo = vehiculo.tipo || 'VEHÍCULO';
          const subcategoria = vehiculo.subcategoria || 'N/A';
          const estado = vehiculo.estado || 'RETENIDO';
          const marca = vehiculo.marca || 'S/M';
          const modelo = vehiculo.modelo || 'S/M';
          const color = vehiculo.color || 'S/C';
          const ano = vehiculo.ano_vehiculo || vehiculo.ano || 'N/A';
          const matricula = vehiculo.Matricula || vehiculo.matricula || 'SIN MATRÍCULA';
          const chasis = vehiculo.chasis || 'SIN CHASIS';
          const conductor = vehiculo.nombre_conductor || 'DESCONOCIDO';
          const ciConductor = vehiculo.ci_conductor || 'N/A';

          const inscriptoNombre = vehiculo['Inscripto a Nombre de'] || vehiculo.inscripto_nombre || 'NO REGISTRA';
          const ciNum = vehiculo['C_I_N°'] || vehiculo.ci_num || 'N/A';
          const fechaIncautacion = vehiculo.fecha_incautacion || 'S/D';
          const unidadCargo = vehiculo.unidad_a_cargo || 'NINGUNA';
          const fiscalCargo = vehiculo.fiscal_a_cargo || 'A DETERMINAR';
          const causa = vehiculo.causa_incautacion || vehiculo.observacion || 'Sin observaciones.';

          // Color dinámico según estado
          let colorEstado = '#f87171'; // Rojo para RETENIDO/INCAUTADO
          if (estado === 'ENTREGADO') colorEstado = '#4ade80'; // Verde
          if (estado === 'DEPOSITADO') colorEstado = '#38bdf8'; // Azul

          return (
            <div key={idItem} style={cardStyle}>
              <div
                onClick={() => toggleTarjeta(idItem)}
                style={{
                  padding: '16px 20px',
                  cursor: 'pointer',
                  userSelect: 'none',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start'
                }}
              >
                <div>
                  <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#38bdf8', marginBottom: '4px' }}>
                    【 {tipo} 】 - {subcategoria} — ESTADO: <span style={{ color: colorEstado }}>{estado}</span>
                  </div>
                  <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#ffffff', marginBottom: '6px' }}>
                    {marca} {modelo} – Color: {color} – Año: {ano}
                  </div>
                  <div style={{ fontSize: '13px', color: '#4ade80', fontWeight: '500', marginBottom: '4px' }}>
                    Chapa/Matrícula: {matricula} | N° de Chasis: {chasis}
                  </div>
                  <div style={{ fontSize: '12px', color: '#a1a1aa' }}>
                    👤 Conductor: {conductor} (C.I.: {ciConductor})
                  </div>
                </div>
                <span style={{ color: '#a1a1aa', fontSize: '18px', paddingLeft: '10px' }}>
                  {estaAbierto ? '▲' : '▼'}
                </span>
              </div>

              {estaAbierto && (
                <div
                  style={{
                    backgroundColor: '#09090b',
                    padding: '15px 20px',
                    borderTop: '1px solid #27272a',
                    fontSize: '13px',
                    color: '#d4d4d8',
                    lineHeight: '1.7'
                  }}
                >
                  <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                    <li>• <strong>ID Registro Interno:</strong> #{idItem}</li>
                    <li>• <strong>Inscripto a Nombre de:</strong> {inscriptoNombre}</li>
                    <li>• <strong>Cédula de Identidad N°:</strong> {ciNum}</li>
                    <li>• <strong>Fecha de Incautación:</strong> {fechaIncautacion}</li>
                    <li>• <strong>Unidad Fiscal Interviniente:</strong> {unidadCargo}</li>
                    <li>• <strong>Fiscal Interviniente:</strong> {fiscalCargo}</li>
                    <li>• <strong>Causa o Motivo de Incautación:</strong> {causa}</li>
                  </ul>
                </div>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}