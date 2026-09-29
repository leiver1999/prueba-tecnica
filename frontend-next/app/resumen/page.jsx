import Link from 'next/link';
import Summary from '../../components/Summary.jsx';
import { summarize } from '../../lib/summary.js';

export default function ResumenPage() {
  // TODO N1/N2: reemplazar estos datos de ejemplo por fetch en el servidor.
  // Consultar API_URL, evitar cache obsoleta y mostrar un error visible sin ceros inventados.
  const counts = summarize([]);
  return <main><p className="eyebrow">RESUMEN / DATOS DE EJEMPLO</p>
    <h1>Resumen de pedidos</h1>
    <p>La conexion a la API esta pendiente.</p>
    <Summary counts={counts} />
    <Link href="/">Volver al inicio</Link>
  </main>;
}
