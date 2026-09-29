import Link from 'next/link';
import Summary from '../../components/Summary.jsx';
import { summarize } from '../../lib/summary.js';

export const dynamic = 'force-dynamic';

export default async function ResumenPage() {
  let counts;
  try {
    const baseUrl = (process.env.API_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');
    const response = await fetch(`${baseUrl}/pedidos`, {
      cache: 'no-store',
      signal: AbortSignal.timeout(5000),
    });
    if (!response.ok) throw new Error('No se pudieron consultar los pedidos');
    const pedidos = await response.json();
    if (!Array.isArray(pedidos)) throw new Error('Respuesta de pedidos no valida');
    counts = summarize(pedidos);
  } catch {
    return <main><p className="eyebrow">RESUMEN DE PEDIDOS</p>
      <h1>Resumen de pedidos</h1>
      <p role="alert">No se pudo cargar el resumen. Comprueba que la API este disponible y vuelve a intentarlo.</p>
      <p><a href="/resumen">Reintentar</a></p>
      <Link href="/">Volver al inicio</Link>
    </main>;
  }

  return <main><p className="eyebrow">RESUMEN DE PEDIDOS</p>
    <h1>Resumen de pedidos</h1>
    <Summary counts={counts} />
    <Link href="/">Volver al inicio</Link>
  </main>;
}
