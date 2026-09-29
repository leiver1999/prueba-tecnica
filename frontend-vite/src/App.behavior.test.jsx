import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, expect, test, vi } from 'vitest';
import App from './App.jsx';
import { api } from './api.js';

vi.mock('./api.js', () => ({ api: { list: vi.fn(), update: vi.fn() } }));
beforeEach(() => { vi.resetAllMocks(); });

const pendiente = { id: 1, cliente: 'Demo A', descripcion: 'Entrega A', estado: 'pendiente' };
const completado = { id: 2, cliente: 'Demo B', descripcion: 'Entrega B', estado: 'completado' };

function diferida() {
  let resolve;
  const promise = new Promise((resolver) => { resolve = resolver; });
  return { promise, resolve };
}

test('consulta el filtro seleccionado y vuelve a consultar Todos sin estado', async () => {
  api.list.mockResolvedValueOnce([pendiente, completado])
    .mockResolvedValueOnce([completado]).mockResolvedValueOnce([pendiente, completado]);
  render(<App />);
  await screen.findByText('Demo A');
  fireEvent.change(screen.getByLabelText('Filtrar por estado'), { target: { value: 'completado' } });
  await screen.findByText('Demo B');
  expect(api.list).toHaveBeenLastCalledWith('completado', expect.objectContaining({ signal: expect.anything() }));
  expect(screen.queryByText('Demo A')).not.toBeInTheDocument();

  fireEvent.change(screen.getByLabelText('Filtrar por estado'), { target: { value: '' } });
  await screen.findByText('Demo A');
  expect(api.list).toHaveBeenLastCalledWith('', expect.objectContaining({ signal: expect.anything() }));
});

test('un error al guardar conserva el estado real y permite intentar otra vez', async () => {
  api.list.mockResolvedValue([pendiente]);
  api.update.mockRejectedValueOnce(new Error('API no disponible'))
    .mockResolvedValueOnce({ ...pendiente, estado: 'completado' });
  render(<App />);
  const fila = (await screen.findByText('Demo A')).closest('tr');
  const selector = screen.getByLabelText('Estado del pedido 1');
  const boton = screen.getByRole('button', { name: 'Guardar pedido 1' });
  fireEvent.change(selector, { target: { value: 'completado' } });
  fireEvent.click(boton);

  expect(await screen.findByRole('alert')).toHaveTextContent('API no disponible');
  expect(api.update).toHaveBeenCalledWith(1, 'completado');
  expect(within(fila).getByText('Pendiente', { selector: '.badge' })).toBeInTheDocument();
  expect(selector).toHaveValue('pendiente');
  expect(boton).toBeEnabled();
  expect(screen.queryByText(/guardado correctamente/)).not.toBeInTheDocument();

  fireEvent.change(selector, { target: { value: 'completado' } });
  fireEvent.click(boton);
  expect(await screen.findByRole('status')).toHaveTextContent('guardado correctamente');
  expect(within(fila).getByText('Completado', { selector: '.badge' })).toBeInTheDocument();
});

test('bloquea doble envio y muestra el estado confirmado por la API', async () => {
  const guardado = diferida();
  api.list.mockResolvedValue([pendiente]);
  api.update.mockReturnValue(guardado.promise);
  render(<App />);
  await screen.findByText('Demo A');
  const selector = screen.getByLabelText('Estado del pedido 1');
  const boton = screen.getByRole('button', { name: 'Guardar pedido 1' });
  fireEvent.change(selector, { target: { value: 'en_proceso' } });
  fireEvent.click(boton);
  fireEvent.click(boton);
  expect(api.update).toHaveBeenCalledTimes(1);
  expect(boton).toBeDisabled();
  expect(boton).toHaveTextContent('Guardando...');
  expect(selector).toBeDisabled();
  expect(screen.getByLabelText('Filtrar por estado')).toBeDisabled();
  expect(screen.getByText('Pendiente', { selector: '.badge' })).toBeInTheDocument();

  await act(async () => { guardado.resolve({ ...pendiente, estado: 'en_proceso' }); });
  expect(screen.getByText('En proceso', { selector: '.badge' })).toBeInTheDocument();
  expect(boton).toBeEnabled();
  expect(selector).toBeEnabled();
  expect(screen.getByLabelText('Filtrar por estado')).toBeEnabled();
});

test('quita del listado el pedido que ya no coincide con el filtro tras guardarlo', async () => {
  api.list.mockResolvedValue([pendiente]);
  api.update.mockResolvedValue({ ...pendiente, estado: 'completado' });
  render(<App />);
  await screen.findByText('Demo A');
  fireEvent.change(screen.getByLabelText('Filtrar por estado'), { target: { value: 'pendiente' } });
  await screen.findByText('Demo A');
  fireEvent.change(screen.getByLabelText('Estado del pedido 1'), { target: { value: 'completado' } });
  fireEvent.click(screen.getByRole('button', { name: 'Guardar pedido 1' }));
  expect(await screen.findByText('No hay pedidos.')).toBeInTheDocument();
  expect(screen.queryByText('Demo A')).not.toBeInTheDocument();
  expect(screen.getByRole('status')).toHaveTextContent('guardado correctamente');
});

test('muestra carga, error y reintento conservando el filtro seleccionado', async () => {
  const carga = diferida();
  api.list.mockReturnValueOnce(carga.promise)
    .mockRejectedValueOnce(new Error('Fallo de conexion')).mockResolvedValueOnce([]);
  render(<App />);
  expect(screen.getByRole('status')).toHaveTextContent('Cargando pedidos');
  await act(async () => { carga.resolve([pendiente]); });
  fireEvent.change(screen.getByLabelText('Filtrar por estado'), { target: { value: 'completado' } });
  expect(await screen.findByRole('alert')).toHaveTextContent('Fallo de conexion');
  expect(screen.queryByText('No hay pedidos.')).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole('button', { name: 'Reintentar carga' }));
  expect(await screen.findByText('No hay pedidos.')).toBeInTheDocument();
  expect(api.list).toHaveBeenLastCalledWith('completado', expect.objectContaining({ signal: expect.anything() }));
  expect(screen.queryByRole('alert')).not.toBeInTheDocument();
});

test('una respuesta antigua no reemplaza los resultados del filtro actual', async () => {
  const antigua = diferida();
  api.list.mockReturnValueOnce(antigua.promise).mockResolvedValueOnce([completado]);
  render(<App />);
  fireEvent.change(screen.getByLabelText('Filtrar por estado'), { target: { value: 'completado' } });
  await screen.findByText('Demo B');
  await act(async () => { antigua.resolve([pendiente, completado]); });
  expect(screen.queryByText('Demo A')).not.toBeInTheDocument();
  expect(screen.getByText('Demo B')).toBeInTheDocument();
});

test('al montar de nuevo consulta el estado persistido por la API', async () => {
  api.list.mockResolvedValueOnce([pendiente])
    .mockResolvedValueOnce([{ ...pendiente, estado: 'completado' }]);
  api.update.mockResolvedValue({ ...pendiente, estado: 'completado' });
  const vista = render(<App />);
  await screen.findByText('Demo A');
  fireEvent.change(screen.getByLabelText('Estado del pedido 1'), { target: { value: 'completado' } });
  fireEvent.click(screen.getByRole('button', { name: 'Guardar pedido 1' }));
  await waitFor(() => expect(screen.getByRole('status')).toHaveTextContent('guardado correctamente'));
  vista.unmount();
  render(<App />);
  await screen.findByText('Demo A');
  expect(screen.getByLabelText('Estado del pedido 1')).toHaveValue('completado');
  expect(screen.getByText('Completado', { selector: '.badge' })).toBeInTheDocument();
  expect(api.list).toHaveBeenCalledTimes(2);
});
