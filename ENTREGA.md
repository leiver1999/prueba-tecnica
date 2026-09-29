# Resumen de entrega

Nombre o identificador de candidato: Jose Valenciano Herrera
Fecha: 29/09/2026
Commit final (si se uso Git): cambios en entrega y uso_IA v3

## Requisitos
P1: Implementado; se eliminan los espacios al inicio y al final de cliente y descripcion. Si alguno queda vacio, la API responde 400 sin insertar el pedido
P2: Implementado; el listado permite filtrar por estado. Sin filtro devuelve todos los pedidos; con un estado valido devuelve solo las coincidencias. Un estado vacio o desconocido devuelve 400
P3: Implementado; se puede actualizar el estado de un pedido y guardar el cambio en SQLite. Devuelve 200 con el pedido actualizado, 400 por estado invalido y 404 si el pedido no existe con una solicitud valida. Los errores de estructura o tipo conservan el 422
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

- Verificacion completa del 29/09/2026: el candidato ejecuto
  `python scripts/verificar.py` desde proyecto_base y compartio la salida.
  Resultado: 48 pruebas aprobadas (35 backend, 3 cliente HTTP, 2 conteos de Next.js
  y 8 componentes Vite), sin fallos. Ambas compilaciones terminaron correctamente.
  Se mantuvo una advertencia de deprecacion de Starlette/AnyIO.
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

- El candidato confirmo el funcionamiento de la validacion de P1 en Swagger.
- El candidato cambio estados y confirmo que los conteos del resumen se actualizaron.

Limitaciones conocidas:

- La persistencia del backend se comprobo reabriendo la aplicacion mediante TestClient;
  el reinicio manual del servidor no fue comprobado por el agente.
- Las pruebas de componentes y del cliente HTTP usan respuestas simuladas.
  Sigue pendiente confirmar la revision manual con teclado.
- Los errores y la recuperacion de Next.js se comprobaron con una API local de
  prueba. Falta confirmar la prueba manual deteniendo solo el backend y
  manteniendo Next.js activo; detener Next.js no comprueba ese comportamiento.

No declarar pruebas aprobadas si no se ejecutaron. No incluir .venv, node_modules,
.next, dist, bases de datos personales ni secretos en el archivo de entrega.
