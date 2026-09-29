import Link from 'next/link';
export default function Home() {
  return <main><p className="eyebrow">NEXT.JS / EJERCICIO COMPLEMENTARIO</p>
    <h1>Panel de resumen</h1><p>Esta aplicacion es independiente de Vite y consume la misma API Python.</p>
    <Link href="/resumen">Abrir resumen de pedidos</Link>
  </main>;
}
