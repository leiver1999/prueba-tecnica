export default function Summary({ counts }) {
  const items = [['total', 'Total'], ['pendiente', 'Pendientes'], ['en_proceso', 'En proceso'], ['completado', 'Completados']];
  return <dl className="cards">{items.map(([key, label]) => <div className="card" key={key}>
    <dt>{label}</dt><dd>{counts[key]}</dd>
  </div>)}</dl>;
}
