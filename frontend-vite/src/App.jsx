import { useEffect, useRef, useState } from 'react';
import { api } from './api.js';
import { ESTADOS, LABELS } from './constants.js';

export default function App() {
  const [pedidos, setPedidos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [estado, setEstado] = useState('');
  const [intento, setIntento] = useState(0);
  const [selecciones, setSelecciones] = useState({});
  const [guardandoId, setGuardandoId] = useState(null);
  const [errorGuardado, setErrorGuardado] = useState('');
  const [aviso, setAviso] = useState('');
  const guardando = useRef(false);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError('');
    setErrorGuardado('');
    setAviso('');
    setSelecciones({});
    api.list(estado, { signal: controller.signal })
      .then((datos) => { if (!controller.signal.aborted) setPedidos(datos); })
      .catch((err) => {
        if (!controller.signal.aborted && err.name !== 'AbortError') setError(err.message);
      })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [estado, intento]);

  async function guardar(pedido) {
    if (guardando.current) return;
    guardando.current = true;
    setGuardandoId(pedido.id);
    setErrorGuardado('');
    setAviso('');
    try {
      const actualizado = await api.update(pedido.id, selecciones[pedido.id] ?? pedido.estado);
      setPedidos((actuales) => actuales
        .map((item) => item.id === actualizado.id ? actualizado : item)
        .filter((item) => !estado || item.estado === estado));
      setSelecciones((actuales) => ({ ...actuales, [pedido.id]: actualizado.estado }));
      setAviso(`Pedido ${pedido.id} guardado correctamente.`);
    } catch (err) {
      setErrorGuardado(`No se pudo guardar el pedido ${pedido.id}: ${err.message}`);
      setSelecciones((actuales) => ({ ...actuales, [pedido.id]: pedido.estado }));
    } finally {
      guardando.current = false;
      setGuardandoId(null);
    }
  }

  return <main className="container">
    <header><p className="eyebrow">PRUEBA JUNIOR / DATOS FICTICIOS</p>
      <h1>Gestion de pedidos</h1><p>React + Vite. API local en Python.</p></header>
    <section className="panel">
      <h2>Pedidos</h2>
      <div className="toolbar">
        <label htmlFor="filtro-estado">Filtrar por estado</label>
        <select id="filtro-estado" value={estado} disabled={guardandoId !== null}
          onChange={(event) => setEstado(event.target.value)}>
          <option value="">Todos</option>
          {ESTADOS.map((valor) => <option key={valor} value={valor}>{LABELS[valor]}</option>)}
        </select>
      </div>
      {loading && <p role="status">Cargando pedidos...</p>}
      {error && <div><p role="alert">{error}</p>
        <button type="button" onClick={() => setIntento((actual) => actual + 1)}>Reintentar carga</button>
      </div>}
      {errorGuardado && <p role="alert">{errorGuardado}</p>}
      {aviso && <p role="status" className="notice">{aviso}</p>}
      {!loading && !error && pedidos.length === 0 && <p>No hay pedidos.</p>}
      {!loading && !error && pedidos.length > 0 && <div className="table-wrap"><table>
        <caption>Pedidos registrados</caption>
        <thead><tr><th scope="col">ID</th><th scope="col">Cliente</th>
          <th scope="col">Descripcion</th><th scope="col">Estado</th><th scope="col">Acciones</th></tr></thead>
        <tbody>{pedidos.map((pedido) => <tr key={pedido.id}>
          <td>{pedido.id}</td><td>{pedido.cliente}</td><td>{pedido.descripcion}</td>
          <td><span className={`badge ${pedido.estado}`}>{LABELS[pedido.estado]}</span></td>
          <td><div className="actions">
            <label htmlFor={`estado-${pedido.id}`}>Estado del pedido {pedido.id}</label>
            <select id={`estado-${pedido.id}`} value={selecciones[pedido.id] ?? pedido.estado}
              disabled={guardandoId !== null} onChange={(event) => {
                setSelecciones((actuales) => ({ ...actuales, [pedido.id]: event.target.value }));
                setErrorGuardado('');
                setAviso('');
              }}>
              {ESTADOS.map((valor) => <option key={valor} value={valor}>{LABELS[valor]}</option>)}
            </select>
            <button type="button" aria-label={`Guardar pedido ${pedido.id}`}
              disabled={guardandoId !== null} onClick={() => guardar(pedido)}>
              {guardandoId === pedido.id ? 'Guardando...' : 'Guardar'}
            </button>
          </div></td>
        </tr>)}</tbody>
      </table></div>}
    </section>
    <footer>La pagina de resumen se implementa por separado en Next.js, puerto 3000.</footer>
  </main>;
}
