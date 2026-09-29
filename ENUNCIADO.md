# Prueba técnica | Desarrollo junior con IA
Python + React / Vite + Next.js

**Duración evaluada: 180 minutos. Preparación del entorno: antes de comenzar.**

Construirás mejoras sobre un gestor de pedidos ficticios. Queremos conocer tus bases, tu capacidad para resolver problemas y cómo diriges y verificas el trabajo de un agente de codificación. No necesitas terminar todo para demostrar habilidades: entrega lo que puedas comprobar y explica lo pendiente.

## Estructura de la sesión

| Minutos | Actividad | IA |
| --- | --- | --- |
| 0-15 | Fundamentos Python, SQL y HTTP | No |
| 15-70 | Parte 1: API Python | Sí |
| 70-80 | Fundamentos React | No |
| 80-130 | Parte 2A: React con Vite | Sí |
| 130-150 | Parte 2B: página Next.js | Sí |
| 150-165 | Cambio de requisito anunciado en vivo | Sí, tras explicar el enfoque |
| 165-180 | Demostración, revisión y defensa | No |

La documentación está permitida, incluso durante fundamentos. En los bloques sin IA, pausa el chat, el agente y las sugerencias generativas del editor. Las pausas por fallas de infraestructura se registran y no cuentan como tiempo evaluado.

## Lo que recibes

Una API FastAPI con SQLite, seis pedidos de ejemplo, listado React funcional, una página Next.js de ejemplo, estilos, cliente HTTP, pruebas iniciales y scripts. La parte frontend contiene **dos aplicaciones independientes**, no una mezcla de Vite dentro de Next.js. Ambas usan la misma API.

**Fuera del alcance:** autenticación, nube, AWS, Docker, despliegues, diseño visual avanzado, creación de agentes personalizados y nuevas dependencias no justificadas. No hay acceso a sistemas productivos ni datos reales.

<!-- PAGE -->
# Parte 1 | Python y API

Trabaja principalmente en `backend/app/main.py`, `repository.py` y `tests/`. La API inicial arranca, crea pedidos y los consulta, pero tiene pendientes intencionales.

| ID | Trabajo solicitado | Aceptación |
| --- | --- | --- |
| P1 | Corregir textos vacíos y normalizar | En POST, recortar espacios de cliente y descripción. Si alguno queda vacío, responder 400 sin insertar. |
| P2 | Filtrar por estado | GET acepta estado opcional. Sin parámetro devuelve todos; con un estado válido, solo coincidencias. Estado desconocido o vacío: 400. |
| P3 | Actualizar estado | PATCH actualiza un pedido existente y devuelve el objeto actualizado con 200. Estado desconocido: 400. ID inexistente con cuerpo válido: 404. |
| P4 | Verificar tu implementación | Agregar al menos tres pruebas nuevas: espacios, filtro y actualización. Conservar las cuatro pruebas iniciales. |

## Reglas de implementación

Los estados iniciales permitidos son `pendiente`, `en_proceso` y `completado`, exactamente en minúsculas. No se requiere convertir variantes de escritura. La creación siempre inicia en `pendiente`.

Los cambios deben persistir en SQLite y mantenerse al reiniciar la API. No reemplaces la base de datos por una lista en memoria. Usa parámetros SQL, no concatenación de entradas en consultas. No cambies los nombres de campos ni el contrato publicado.

Una respuesta de error debe ser visible y consistente. Para errores de negocio, usa `{"detail": "mensaje comprensible"}`. La estructura o los tipos de entrada incorrectos conservan el 422 de la validación del framework.

## Comprobaciones mínimas

Prueba una operación correcta y una incorrecta. Confirma que una solicitud rechazada no inserta ni modifica datos. Para el filtro, usa registros de más de un estado. Para persistencia, vuelve a consultar el pedido y reinicia el servicio con la misma base.

FastAPI permite probar la aplicación con `TestClient` y pytest, sin mantener un servidor externo ejecutándose. El repositorio ya incluye esa configuración.

**No se requieren clases adicionales, un ORM ni arquitectura compleja.** Se acepta una solución sencilla que puedas explicar y verificar.

<!-- PAGE -->
# Parte 2 | React, Vite y Next.js

## 2A. React con Vite

El listado y el cliente HTTP ya existen. Completa la interfaz conservando la separación entre datos, estado y presentación.

| ID | Trabajo solicitado | Aceptación |
| --- | --- | --- |
| F1 | Filtro por estado | Selector Todos / Pendiente / En proceso / Completado. Debe consultar la API con el parámetro seleccionado, no solo filtrar una lista fija. |
| F2 | Cambio de estado por pedido | Selector y botón Guardar. Enviar PATCH real y reflejar la respuesta. Tras recargar, conservar el cambio. |
| F3 | Estados de interfaz | Mostrar carga, lista vacía y error; bloquear doble envío mientras se guarda. No mostrar éxito cuando la API falla. Permitir reintentar una carga fallida. |
| F4 | Pruebas y uso accesible | Dos pruebas nuevas: filtro y error al guardar. Etiquetas de controles, claves estables y uso con teclado. |

Si un pedido cambia y deja de coincidir con el filtro activo, debe dejar de mostrarse. Ante un error de guardado, conserva su estado real. Puedes recargar la lista o actualizarla inmutablemente tras una respuesta exitosa.

No se solicita formulario de creación: puedes crear pedidos desde la documentación interactiva de la API. Los estilos base ya están incluidos; no se calificará una apariencia sofisticada.

## 2B. Next.js: un ejercicio acotado

| ID | Trabajo solicitado | Aceptación |
| --- | --- | --- |
| N1 | Conectar `/resumen` | Consultar GET pedidos desde el servidor Next.js y mostrar total, pendientes, en proceso y completados. Usar `API_URL`. |
| N2 | Actualidad y error | Recargar la página debe consultar datos actuales. Si la API falla, mostrar un error, no ceros presentados como un resultado real. |

Puedes reutilizar `components/Summary.jsx` y `lib/summary.js`, ya resueltos. No dupliques toda la aplicación Vite en Next.js. Explica dónde se ejecuta la consulta y por qué esta página no necesita hooks de interacción. En App Router, páginas y layouts son Server Components por defecto.

**Datos iniciales:** total 6; pendientes 3; en proceso 2; completados 1. Estos números cambiaran cuando modifiques pedidos.

<!-- PAGE -->
# Fundamentos y uso del agente

## Bloques sin IA

**Python, SQL y HTTP - 15 minutos.** Abre `ejercicios/fundamentos.py`, ejecuta la función y corrige el conteo de pendientes. Demuestra una lista vacía y una con dos pendientes. Explica el efecto del retorno dentro del bucle. Escribe una consulta parametrizada para listar pedidos pendientes y diferencia 400, 404 y 422 dentro de este contrato.

**React - 10 minutos.** Analiza `ejercicios/react_estado.jsx.txt`. Explica la mutación del estado, propone una actualización inmutable y contempla un ID inexistente. Describe brevemente la diferencia entre Vite y Next.js y dónde se ejecuta el fetch de cada aplicación.

Registra las respuestas en `RESPUESTAS.md`. No se exige memorizar sintaxis: puedes consultar documentación y ejecutar ejemplos.

## Bloques con IA

Utiliza un agente con capacidad de leer el proyecto, proponer o aplicar cambios y apoyar la ejecución de pruebas. Debes mostrar al menos un ciclo completo: objetivo, contexto, plan, permisos, cambios revisados y comprobación. No basta con pegar código de un chat sin entenderlo.

Agrega al menos tres instrucciones específicas a `AGENTS.md` y explica cómo las cargaste en tu herramienta. No necesitas conocer configuraciones de todas las marcas. Si la herramienta no lee ese archivo automáticamente, incorpóralo como contexto y documéntalo.

Antes de aceptar un comando, revisa su propósito, alcance y archivos afectados. No facilites credenciales ni permitas acciones fuera del proyecto. Revisa el diff y valida la salida del agente: esa responsabilidad sigue siendo humana.

## Evidencia esperada

Completa `USO_IA.md` con la herramienta utilizada, la tarea delegada, un extracto relevante de la instrucción, los cambios revisados y los comandos realmente ejecutados. La segunda tarea de la plantilla es opcional.

No necesitamos chats personales completos, una suscripción propia ni el razonamiento interno del modelo. Si no hay acceso a una herramienta aprobada, avísalo antes de comenzar para que se facilite una alternativa equivalente.

<!-- PAGE -->
# Contrato HTTP y datos

Base local: `http://127.0.0.1:8000`. Documentación interactiva: `/docs`.

| Método y ruta | Entrada | Salida esperada |
| --- | --- | --- |
| GET `/health` | Sin cuerpo | 200: estado del servicio. Ya implementado. |
| GET `/pedidos` | Estado opcional en query | 200: array de pedidos; 400 si estado no es válido. |
| GET `/pedidos/{id}` | ID entero | 200: un pedido; 404 si no existe. Ya implementado. |
| POST `/pedidos` | Cliente y descripción | 201: pedido creado; 400 por texto vacío; 422 por estructura o tipo. |
| PATCH `/pedidos/{id}/estado` | Un estado | 200: pedido actualizado; 400 por estado; 404 por ID inexistente; 422 por estructura o tipo. |

## Ejemplos de cuerpos

Creación:
```json
{"cliente": "Cliente Demo", "descripcion": "Entrega ficticia"}
```
Actualización:
```json
{"estado": "en_proceso"}
```
Respuesta de pedido:
```json
{"id": 1, "cliente": "Cliente Demo", "descripcion": "Entrega ficticia", "estado": "pendiente"}
```

## Detalles para evitar ambigüedades

Cliente y descripción son cadenas obligatorias, con máximos de 100 y 300 caracteres respectivamente. Esos límites y los tipos se validan antes de la normalización. Campos faltantes, tipos incorrectos, campos extra o exceso de longitud producen 422. Un texto vacío o formado por espacios produce 400. El ID debe ser entero; una ruta con un ID no entero conserva 422.

`GET /pedidos` devuelve todos; `GET /pedidos?estado=` devuelve 400. No se exige paginación, búsqueda por texto, fechas ni eliminación de pedidos.

El evaluador entregará un cambio pequeño durante la sesión. Sus criterios se explicarán al entregarlo y no se calificarán antes. No hay otros requisitos funcionales ocultos.

<!-- PAGE -->
# Entrega y criterios de evaluación

## Entrega

Incluye el proyecto modificado, tus pruebas, `RESPUESTAS.md`, `USO_IA.md`, `ENTREGA.md` y las instrucciones nuevas de `AGENTS.md`. Anota resultados reales, limitaciones y cualquier requisito incompleto. Conserva los archivos de bloqueo de dependencias generados durante la preparación.

Puedes usar Git para registrar cambios comprensibles. No se califica el número de commits, prompts ni líneas generadas. Antes de enviar, revisa los archivos incluidos y usa `scripts/empaquetar_entrega.py` para excluir dependencias, entornos, secretos y datos locales.

## Rúbrica conocida desde el inicio

| Criterio | Peso |
| --- | --- |
| Fundamentos y comprensión | 15 |
| Python y API | 20 |
| React con Vite | 20 |
| Next.js | 10 |
| Pruebas y depuración | 10 |
| Uso responsable de IA y agentes | 20 |
| Git, documentación y comunicación | 5 |
| **Total** | **100** |

Cada criterio usa nivel 0 a 4: 0 sin evidencia; 1 con guía detallada; 2 parcial con ayuda frecuente; 3 cumple con ayuda puntual; 4 cumple con autonomía y explica decisiones y límites. Los puntos se calculan como peso por nivel dividido entre cuatro.

Criterio orientativo: 70/100, con nivel mínimo 3 en fundamentos y en IA. No es una decisión automática de contratación. Se valoran evidencias de trabajo y comprensión, no velocidad por si sola.

## Defensa final

Muestra un cambio importante, una prueba que lo comprueba y una decisión tomada frente al agente. Explica lo que no se pudo validar. Revisarás una propuesta simulada incorrecta y responderás que aceptarías, que rechazarías y cómo lo comprobarías.

**No declares que una prueba pasó si no la ejecutaste. Una entrega parcial explicada es mejor que un resultado aparentemente completo que no puedes defender.**

## Puesta en marcha

Sigue el `README.md` de esta carpeta para instalar, ejecutar, verificar y empaquetar la entrega.
