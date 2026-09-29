import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createApi } from '../src/api-core.js';

test('listado utiliza el filtro enviado', async () => {
  const calls = [];
  const api = createApi('http://local/', async (url) => {
    calls.push(url); return new Response('[]', { status: 200 });
  });
  assert.deepEqual(await api.list('en_proceso'), []);
  assert.equal(calls[0], 'http://local/pedidos?estado=en_proceso');
});

test('el cliente no convierte un HTTP 400 en exito', async () => {
  const api = createApi('http://local', async () => new Response(
    JSON.stringify({ detail: 'Estado no valido' }), { status: 400 }));
  await assert.rejects(api.update(1, 'pendiente'), (error) => error.status === 400 && error.message === 'Estado no valido');
});

test('PATCH envia el JSON y metodo correctos', async () => {
  let call;
  const api = createApi('http://local', async (url, options) => {
    call = { url, options }; return new Response('{"id":2,"estado":"completado"}');
  });
  await api.update(2, 'completado');
  assert.equal(call.url, 'http://local/pedidos/2/estado');
  assert.equal(call.options.method, 'PATCH');
  assert.deepEqual(JSON.parse(call.options.body), { estado: 'completado' });
});
