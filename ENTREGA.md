# Resumen de entrega

Nombre o identificador de candidato: Jose Valenciano Herrera
Fecha: 
Commit final (si se uso Git):

## Requisitos
P1:
P2:
P3:
P4: Completado. Se conservan las cuatro pruebas iniciales de test_base.py.
Se agregaron pruebas de espacios (test_validacion_textos.py), filtro
(test_filtro.py) y actualizacion (test_actualizacion.py).
F1: Implementado. Selector de estado que consulta la API; Todos omite el filtro.
F2: Implementado. Selector y Guardar por pedido, PATCH mediante el cliente HTTP,
actualizacion con la respuesta y retirada de filas que ya no coinciden con el filtro.
F3: Implementado. Carga, lista vacia, errores, reintento de carga y bloqueo durante
el guardado. Un fallo conserva el estado confirmado y no muestra exito.
F4: Implementado. Se conserva la prueba inicial y se agregan siete pruebas de
comportamiento, incluidas filtro y error al guardar. Controles nativos con etiquetas,
botones con nombres por pedido y claves estables. Pendiente revision manual con teclado.
N1: Implementado. /resumen consulta GET /pedidos desde el servidor Next.js usando
API_URL y reutiliza summarize y Summary para mostrar los cuatro conteos.
N2: Implementado. Pagina dinamica y fetch sin cache; muestra un error con enlace
para reintentar si la API falla, sin presentar ceros como un resultado real.
Cambio en vivo:

## Verificación
Comandos ejecutados y resultados reales:
- Desde backend: `..\.venv\Scripts\python.exe -m pytest -q`.
  Resultado al completar P4: 35 pruebas aprobadas (4 iniciales y 31 casos nuevos),
  con una advertencia de deprecacion de Starlette/AnyIO.
  Las pruebas usan bases SQLite temporales.
- Desde frontend-vite: `npm.cmd test`: 8 pruebas de componentes aprobadas;
  `npm.cmd run test:logic`: 3 pruebas del cliente HTTP aprobadas;
  `npm.cmd run build`: compilacion de Vite completada.
- Desde frontend-next: `npm.cmd test`: 2 pruebas aprobadas;
  `npm.cmd run build`: compilacion correcta, /resumen renderizado bajo demanda.
  Se ejecuto una comprobacion HTTP con `node --input-type=module -`, iniciando la
  pagina compilada y una API local de prueba en puertos libres: ocho comprobaciones
  correctas de conteos, actualidad, lista vacia, errores y recuperacion.
Casos manuales revisados:
Limitaciones conocidas:
- La persistencia del backend se comprobo reabriendo la aplicacion mediante TestClient;
  el reinicio manual del servidor no fue comprobado por el agente.
- Las pruebas de componentes y del cliente HTTP usan respuestas simuladas. Falta
  comprobar Vite y la API juntos en el navegador, recargar tras guardar y revisar
  el uso con teclado. La compilacion de Vite no sustituye esa comprobacion.
- Next.js se comprobo por HTTP contra una API local de prueba con respuestas
  controladas; falta comprobar sus conteos con los pedidos reales del ejercicio
  y revisar la pagina visualmente en el navegador.

No declarar pruebas aprobadas si no se ejecutaron. No incluir .venv, node_modules,
.next, dist, bases de datos personales ni secretos en el archivo de entrega.
