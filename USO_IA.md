# Registro de uso de IA de esta prueba

No incluir conversaciones privadas, credenciales ni datos de otras empresas.
No hace falta copiar todo el chat ni informar razonamientos internos del modelo.

## Herramienta y acceso
Agente/editor/versión disponible (si se conoce):
Agente de codificacion de esta conversacion; version exacta no registrada.
Como verificaste las instrucciones de AGENTS.md:
Despues de agregar las tres reglas del proyecto, el agente ejecuto
`Get-Content -Encoding UTF8 AGENTS.md` y recibio el contenido completo actualizado.
La lectura explicita incorporo las reglas al contexto de esta conversacion; no se
afirma que se comprobo su carga automatica. El agente confirmo estas reglas:
respetar el contrato HTTP de pedidos, usar SQLite con parametros y pruebas
temporales, y separar las consultas de Vite/navegador y Next.js/servidor.

## Tarea delegada 1
Objetivo y contexto que compartiste:
Instrucción o extracto relevante:
Plan del agente y decisión humana:
Archivos/comandos que autorizaste:
Cambio revisado en el diff:
Comprobación ejecutada y resultado real:

## Tarea delegada 2 o corrección
Objetivo y contexto:
Cambio aceptado/rechazado o corregido y motivo:
Evidencia de comprobación:

## Permisos y limites
Acciones para las que requeriste confirmación:
Como limitaste el acceso al proyecto:

## Limites de la entrega
Que no pudiste validar, que quedo pendiente y siguiente paso:

## Evidencia de P2 (2026-09-28)

- Herramienta: agente de codificacion de esta conversacion.
- Solicitud del candidato: "sigamos con p2, ya funciona" (P1 comprobado por el candidato).
- Contexto leido explicitamente por el agente: AGENTS.md, README.md, ENUNCIADO.md,
  codigo del backend y pruebas existentes. Las tres reglas nuevas del candidato en
  AGENTS.md siguen pendientes.
- Plan aplicado: reutilizar ESTADOS, validar el parametro en main.py, filtrar en
  repository.py con SQL parametrizado y agregar pruebas con SQLite temporal.
- Archivos modificados para P2: backend/app/main.py, backend/app/repository.py,
  backend/tests/test_filtro.py y este registro. Revision humana de los cambios: pendiente.
- Comando ejecutado desde backend: `..\.venv\Scripts\python.exe -m pytest -q`.
  El primer intento fallo por permisos de acceso al directorio temporal de pytest.
  Se solicito ejecucion fuera del entorno restringido y se repitio el comando:
  **14 pruebas aprobadas**, incluidas las cuatro iniciales y diez casos nuevos de P2.
  Hubo una advertencia de deprecacion de una dependencia (Starlette/AnyIO).
- Casos comprobados: tres estados validos con datos variados, listado sin filtro,
  filtro sin coincidencias y rechazo con 400 de estados vacios o desconocidos,
  verificando que los rechazos no alteran los datos.
- Limite: no se comprobo P2 en el navegador ni se ejecutaron pruebas del frontend
  en esta tarea. P3 sigue pendiente.

## Evidencia de P3 (2026-09-28)

- Solicitud del candidato: "me puedes hacer estos cambios porfa", referida a P3.
- El agente volvio a leer AGENTS.md y el codigo actual del backend y sus fixtures.
  README.md y ENUNCIADO.md ya se habian leido durante P2.
- Plan aplicado: validar el estado, actualizar SQLite con parametros y devolver
  el pedido actualizado; responder 404 si no existe. Mantener la validacion 422.
- Archivos modificados: backend/app/main.py, backend/app/repository.py,
  backend/tests/test_actualizacion.py y este registro.
- SQL utilizado: `UPDATE pedidos SET estado = ? WHERE id = ?`.
  La actualizacion y la consulta del resultado usan la misma conexion y transaccion.
- Comando ejecutado desde backend: `..\.venv\Scripts\python.exe -m pytest -q`.
  Se solicito ejecucion fuera del entorno restringido por el problema de acceso
  al directorio temporal ya comprobado en P2.
- Resultado: **27 pruebas aprobadas**, incluidas las 14 anteriores y 13 casos
  nuevos. Una advertencia de deprecacion de Starlette/AnyIO.
- Se comprobaron estados validos, repetir el mismo estado, conservar otros campos
  y pedidos, errores 400/404/422 sin alterar datos y persistencia al cerrar un
  TestClient y crear otra aplicacion con la misma base SQLite temporal.
- Limites: revision humana pendiente; no se reinicio el proceso del servidor
  manual ni se comprobo Swagger en esta tarea. No se ejecutaron pruebas frontend.
  Las pruebas especificas de espacios de P1 requeridas por P4 siguen pendientes.

## Evidencia de P4 (2026-09-28)

- Solicitud del candidato: automatizar las pruebas de espacios que faltaban
  para P4, complementando las de filtro y actualizacion ya agregadas.
- El agente leyo explicitamente AGENTS.md y reviso la implementacion actual,
  la fixture client y las cuatro pruebas iniciales antes del cambio.
- Se agrego backend/tests/test_validacion_textos.py con ocho casos: recorte de
  extremos y consulta de los valores guardados, rechazo de cadenas vacias,
  espacios, tabulaciones y saltos de linea en cada campo, y ambos campos en blanco.
  Se comprueba que los rechazos no insertan ni modifican pedidos existentes.
- No se cambio el codigo de la aplicacion ni las pruebas existentes.
- Comando ejecutado desde backend: `..\.venv\Scripts\python.exe -m pytest -q`.
  Se solicito acceso fuera del entorno restringido a la carpeta temporal de pytest,
  como en P2 y P3. Resultado: **35 pruebas aprobadas**, con una advertencia de
  deprecacion de Starlette/AnyIO. Se usaron bases temporales.
- Se actualizo ENTREGA.md con el estado de P4 y el resultado real.
- Limites: revision humana de las nuevas pruebas pendiente; no se ejecutaron
  pruebas de frontend ni builds. Las tres reglas nuevas de AGENTS.md siguen pendientes.

## Evidencia de F1-F4 (2026-09-28)

- Solicitud del candidato: ayuda para completar filtro, guardado, estados de
  interfaz, pruebas y accesibilidad de React con Vite.
- Se leyo AGENTS.md y se revisaron los criterios F1-F4 de ENUNCIADO.md, App.jsx,
  el cliente HTTP, las constantes, estilos, configuracion y pruebas existentes.
- Plan aplicado: reutilizar api.list y api.update; separar la seleccion provisional
  del estado confirmado; actualizar la lista solo al recibir exito y quitar el
  pedido si deja de coincidir con el filtro. Bloquear controles durante el guardado.
- Cambios: frontend-vite/src/App.jsx y nuevo App.behavior.test.jsx; registro en
  ENTREGA.md y este archivo. Se conservaron las pruebas originales y dependencias.
- Se cancelan las cargas anteriores al cambiar el filtro y se ignoran sus respuestas.
  Los errores de carga permiten reintentar. Un error al guardar restaura la seleccion
  al estado confirmado y muestra el mensaje de error sin anunciar exito.
- Comandos ejecutados desde frontend-vite: `npm.cmd test` (8 aprobadas),
  `npm.cmd run test:logic` (3 aprobadas) y `npm.cmd run build` (compilacion correcta).
- Siete pruebas nuevas cubren filtro y Todos, error de guardado y reintento,
  bloqueo de doble envio, retirada de una fila fuera del filtro, carga/error/vacio,
  respuestas antiguas y consulta del estado al montar de nuevo.
- Limites: las pruebas usan respuestas simuladas; no se realizo la comprobacion
  integrada en el navegador ni la revision manual con teclado. Revision humana
  de cambios pendiente. Next.js y las tres reglas nuevas de AGENTS.md siguen pendientes.

## Evidencia de N1-N2 (2026-09-28)

- Solicitud del candidato: implementar la conexion y manejo de errores de /resumen.
- El agente leyo AGENTS.md, los criterios N1/N2 y la configuracion descrita en
  README.md. Reviso la pagina Next.js, Summary, summarize y las pruebas existentes.
- Cambio aplicado en frontend-next/app/resumen/page.jsx: Server Component async
  que consulta API_URL/pedidos, con cache no-store y pagina force-dynamic. Se conserva
  el calculo y la presentacion existentes. No necesita hooks porque la consulta
  ocurre en el servidor y la pagina no tiene estado interactivo de cliente.
- Se comprueba el estado HTTP y que el JSON sea una lista. Un fallo de red, de HTTP
  o de lectura de datos muestra un aviso y Reintentar, sin mostrar las tarjetas.
  El fetch tiene un limite de cinco segundos para no esperar indefinidamente.
- Comandos desde frontend-next: `npm.cmd test` (2 pruebas aprobadas) y
  `npm.cmd run build` (correcto; /resumen aparece como dinamico).
- Se ejecuto un script por entrada estandar con `node --input-type=module -`:
  inicio una API HTTP local de prueba y un proceso Next.js con la compilacion
  generada en puertos libres, y cerro ambos al terminar. No detuvo los servicios
  del candidato ni modifico pedidos. API_URL se cambio solo en el proceso de prueba.
- Ocho comprobaciones HTTP correctas: conteos iniciales, nueva consulta y cambio
  de conteos al recargar, lista vacia real, HTTP 503, JSON invalido, objeto en lugar
  de lista, recuperacion tras fallo y API desconectada. Los fallos mostraron el
  aviso sin tarjetas de conteos.
- Se actualizo ENTREGA.md. Limites: revision humana pendiente; no se reviso la
  pagina en un navegador ni se comparo con la base manual del candidato. Las tres
  reglas nuevas de AGENTS.md siguen pendientes.

## Incorporacion de reglas a AGENTS.md (2026-09-28)

- Se agregaron tres reglas basadas en README.md y ENUNCIADO.md: contrato de pedidos,
  persistencia y pruebas en SQLite, y separacion de Vite y Next.js.
- Se conservaron las instrucciones originales. El agente volvio a leer el archivo
  actualizado con `Get-Content -Encoding UTF8 AGENTS.md` y confirmo las reglas.
- Esta incorporacion se hizo despues de implementar P1-P4, F1-F4 y N1-N2. Las notas
  anteriores que las indican como pendientes describen el estado de esas tareas
  en ese momento; no son evidencia de que las reglas nuevas se leyeran antes.
- Solo se modificaron AGENTS.md y USO_IA.md; no se ejecutaron pruebas porque el
  cambio fue de documentacion. Revision del candidato de las reglas pendiente.
