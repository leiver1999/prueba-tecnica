import { test } from 'node:test';
import assert from 'node:assert/strict';
import { summarize } from '../lib/summary.js';

test('cuenta una lista vacia', () => {
  assert.deepEqual(summarize([]), { total: 0, pendiente: 0, en_proceso: 0, completado: 0 });
});

test('cuenta los tres estados sin mezclar el total', () => {
  const result = summarize([{ estado: 'pendiente' }, { estado: 'pendiente' }, { estado: 'en_proceso' }, { estado: 'completado' }]);
  assert.deepEqual(result, { total: 4, pendiente: 2, en_proceso: 1, completado: 1 });
});
