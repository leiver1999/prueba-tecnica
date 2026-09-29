import { useEffect, useState } from 'react';
import { api } from './api.js';
import { LABELS } from './constants.js';

export default function App() {
  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const controller = new AbortController();
    api.list('', { signal: controller.signal })
      .then(setPedidos)
      .catch((err) => { if (err.name !== 'AbortError') setError(err.message); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, []);

  return <main className="container">
    <header><p className="eyebrow">PRUEBA JUNIOR / DATOS FICTICIOS</p>
      <h1>Gestion de pedidos</h1><p>React + Vite. API local en Python.</p></header>
    <section className="panel">
      <h2>Pedidos</h2>
      {/* TODO F1: filtro por estado que consulte la API. */}
      {loading && <p role="status">Cargando pedidos...</p>}
      {error && <p role="alert">{error}</p>}
      {!loading && !error && pedidos.length === 0 && <p>No hay pedidos.</p>}
      {!loading && !error && pedidos.length > 0 && <div className="table-wrap"><table>
        <caption>Pedidos registrados</caption>
        <thead><tr><th>ID</th><th>Cliente</th><th>Descripcion</th><th>Estado</th></tr></thead>
        <tbody>{pedidos.map((pedido) => <tr key={pedido.id}>
          <td>{pedido.id}</td><td>{pedido.cliente}</td><td>{pedido.descripcion}</td>
          <td><span className={`badge ${pedido.estado}`}>{LABELS[pedido.estado]}</span></td>
        </tr>)}</tbody>
      </table></div>}
      {/* TODO F2/F3: cambio de estado, confirmacion, error y bloqueo durante la solicitud. */}
    </section>
    <footer>La pagina de resumen se implementa por separado en Next.js, puerto 3000.</footer>
  </main>;
}
