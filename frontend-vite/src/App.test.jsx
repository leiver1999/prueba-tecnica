import { render, screen } from '@testing-library/react';
import { beforeEach, expect, test, vi } from 'vitest';
import App from './App.jsx';
import { api } from './api.js';

vi.mock('./api.js', () => ({ api: { list: vi.fn(), update: vi.fn() } }));
beforeEach(() => { vi.clearAllMocks(); });

test('muestra los pedidos devueltos por la API', async () => {
  api.list.mockResolvedValue([{ id: 1, cliente: 'Demo', descripcion: 'Entrega', estado: 'pendiente' }]);
  render(<App />);
  expect(await screen.findByText('Demo')).toBeInTheDocument();
});

// TODO F4: agregar al menos dos pruebas nuevas de comportamiento (filtro y error al guardar).
