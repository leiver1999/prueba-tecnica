/** Funcionalidad auxiliar ya resuelta; no es necesario reescribirla. */
export function summarize(pedidos) {
  const counts = { total: pedidos.length, pendiente: 0, en_proceso: 0, completado: 0 };
  for (const pedido of pedidos) {
    if (Object.hasOwn(counts, pedido.estado) && pedido.estado !== 'total') counts[pedido.estado] += 1;
  }
  return counts;
}
