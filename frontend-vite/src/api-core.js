/** Cliente independiente de Vite: permite pruebas con node --test sin instalar paquetes. */
export function createApi(baseUrl, fetchImpl = globalThis.fetch) {
  const base = baseUrl.replace(/\/+$/, '');
  async function request(path, options = {}) {
    const response = await fetchImpl(`${base}${path}`, {
      ...options,
      headers: { ...(options.body ? { 'Content-Type': 'application/json' } : {}), ...options.headers },
    });
    const data = await response.json().catch(() => null);
    if (!response.ok) {
      const detail = typeof data?.detail === 'string' ? data.detail : `Error HTTP ${response.status}`;
      const error = new Error(detail);
      error.status = response.status;
      throw error;
    }
    return data;
  }
  return {
    list(estado = '', options = {}) {
      const query = estado ? `?estado=${encodeURIComponent(estado)}` : '';
      return request(`/pedidos${query}`, options);
    },
    update(id, estado, options = {}) {
      return request(`/pedidos/${encodeURIComponent(id)}/estado`, {
        ...options, method: 'PATCH', body: JSON.stringify({ estado }),
      });
    },
  };
}
