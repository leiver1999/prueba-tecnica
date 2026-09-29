# Instrucciones del proyecto de evaluación

Este repositorio es un ejercicio local con datos ficticios, no un sistema productivo.
Lee README.md y el enunciado antes de proponer cambios. No inventes requisitos.
No elimines ni debilites pruebas existentes para hacerlas pasar.
No accedas a credenciales, cuentas reales ni archivos ajenos a este proyecto.
No hagas push, despliegues, instalaciones globales o borrados sin autorización humana.

## Instrucciones que agregara el candidato

Completa esta sección con al menos tres reglas utiles y especificas del proyecto.
Explica como verificaste que tu herramienta las leyo. Si tu herramienta no carga
AGENTS.md automaticamente, incorporalo explicitamente como contexto y documentalo.
No se evalua memorizar rutas propias de una marca de agente.

### Reglas especificas del proyecto

1. Respeta el contrato de pedidos: usa los estados `pendiente`, `en_proceso` y
   `completado` exactamente como estan escritos. En POST, recorta los extremos de
   cliente y descripcion y rechaza con 400 los textos que queden vacios. Conserva
   el 422 para errores de estructura o tipo y el 404 para pedidos inexistentes
   con una solicitud valida.
2. Guarda los cambios en SQLite mediante consultas parametrizadas con `?`, sin
   concatenar entradas ni sustituir la base por una lista en memoria. En pruebas
   de backend usa bases temporales y comprueba que las solicitudes rechazadas no
   insertan ni modifican datos. No uses la base manual para pruebas automaticas.
3. Manten separadas las dos aplicaciones frontend: Vite consulta la API desde el
   navegador con `VITE_API_URL`; Next.js consulta desde el servidor con `API_URL`.
   En `/resumen`, consulta datos actuales al recargar y muestra un error si falla
   la API, sin presentar ceros como si fueran un resultado correcto.

### Como comprobar la lectura

Despues de modificar este archivo, pide al agente que lo lea explicitamente y
resuma las tres reglas. Registra en USO_IA.md el comando o mecanismo utilizado y
lo que el agente confirmo. No declares una carga automatica si no la comprobaste.
