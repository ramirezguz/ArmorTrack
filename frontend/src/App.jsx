import { useState, useEffect } from 'react';
// Importamos el nuevo componente
import VistaRegistro from '../component/VistaRegistro'; 
import VistaEntrega from '../component/VistaEntrega';
import VistaReportes from '../component/VistaReportes';

// --- COMPONENTE: BARRA LATERAL (SIDEBAR) ---
function Sidebar({ vistaActual, setVistaActual }) {
  const botones = [
    { id: 'inicio', label: '🏠 Inicio' },
    { id: 'registro', label: '📝 Ingresar / Incautar' },
    { id: 'entrega', label: '🚚 Entregar Vehículo' },
    { id: 'reportes', label: '📊 Reportes / Consultas' },
  ];

  return (
    <aside style={{ width: '250px', backgroundColor: '#1e293b', color: '#fff', minHeight: '100vh', padding: '1.5rem 1rem' }}>
      <h2 style={{ fontSize: '1.4rem', color: '#38bdf8', marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        🛡️ ARMORTRACK
      </h2>
      <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {botones.map((btn) => (
          <button
            key={btn.id}
            onClick={() => setVistaActual(btn.id)}
            style={{
              padding: '0.75rem 1rem',
              textAlign: 'left',
              backgroundColor: vistaActual === btn.id ? '#0284c7' : 'transparent',
              color: '#fff',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: vistaActual === btn.id ? 'bold' : 'normal',
              transition: 'background-color 0.2s'
            }}
          >
            {btn.label}
          </button>
        ))}
      </nav>
    </aside>
  );
}

// --- VISTA: DASHBOARD / INICIO ---
function VistaInicio() {
  const [stats, setStats] = useState({ total: 0, vehiculos: 0, motos: 0 });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/estadisticas')
      .then((res) => res.json())
      .then((data) => setStats(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h1 style={{ color: '#0f172a', marginBottom: '0.5rem', lineHeight: '1.2', fontSize: '2rem' }}>
        Sistema de Control de Inventario
      </h1>
      <p style={{ color: '#64748b', marginTop: '0.25rem' }}>
        Bienvenido al panel web oficial de ARMORTRACK.
      </p>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginTop: '2rem' }}>
        <div style={cardStyle('#0284c7')}>
          <h3 style={{ fontSize: '1rem', color: '#475569' }}>📋 Total Rodados</h3>
          <p style={numberStyle}>{stats.total}</p>
        </div>
        <div style={cardStyle('#16a34a')}>
          <h3 style={{ fontSize: '1rem', color: '#475569' }}>🚗 Automotores</h3>
          <p style={numberStyle}>{stats.vehiculos}</p>
        </div>
        <div style={cardStyle('#d97706')}>
          <h3 style={{ fontSize: '1rem', color: '#475569' }}>🏍️ Motocicletas</h3>
          <p style={numberStyle}>{stats.motos}</p>
        </div>
      </div>
    </div>
  );
}

// --- COMPONENTE PRINCIPAL ---
export default function App() {
  const [vistaActual, setVistaActual] = useState('inicio');

  return (
    <div style={{ display: 'flex', minHeight: '100vh', fontFamily: 'system-ui, sans-serif', backgroundColor: '#f8fafc' }}>
      <Sidebar vistaActual={vistaActual} setVistaActual={setVistaActual} />
      
      <main style={{ flex: 1, padding: '2.5rem 3rem' }}>
        {vistaActual === 'inicio' && <VistaInicio />}
        {vistaActual === 'registro' && <VistaRegistro />}
        {vistaActual === 'entrega' && <VistaEntrega />}
        {vistaActual === 'reportes' && <VistaReportes />}
      </main>
    </div>
  );
}

// Estilos auxiliares
const cardStyle = (borderColor) => ({
  backgroundColor: '#ffffff',
  padding: '1.5rem',
  borderRadius: '8px',
  borderLeft: `6px solid ${borderColor}`,
  boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
});

const numberStyle = {
  fontSize: '2.2rem',
  fontWeight: 'bold',
  margin: '0.5rem 0 0 0',
  color: '#1e293b'
};