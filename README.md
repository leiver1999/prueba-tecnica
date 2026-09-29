# Proyecto base | Preparación y ejecución

Lee `ENUNCIADO.md` antes de empezar. Sigue estos pasos antes del tiempo evaluado.

## 1. Objetivo y estructura

Todo funciona localmente con datos ficticios. Son dos partes evaluadas y tres procesos: API Python, SPA React/Vite y página Next.js. La aplicación Next no usa el servidor de Vite.

```text
proyecto_base/
  backend/             FastAPI, SQLite, pytest
  frontend-vite/       React, cliente HTTP, Vitest y pruebas Node
  frontend-next/       App Router, resumen y pruebas Node
  ejercicios/          Fragmentos para bloques sin IA
  scripts/             Preparar, ejecutar, verificar, empaquetar
  AGENTS.md            Instrucciones del agente
  ENUNCIADO.md          Prueba publica completa
  RESPUESTAS.md         Respuestas de fundamentos
  USO_IA.md             Evidencia del trabajo con el agente
  ENTREGA.md            Estado final y limitaciones
```

## 2. Requisitos previos

Python 3.11 o superior; preferencia operativa por 3.12 o 3.13. Node.js 22.12 o superior de una rama compatible (22 o 24), npm y Git. Un editor y un agente aprobados por la empresa.

No se incluyen intérpretes, node_modules ni entornos virtuales. La primera instalación necesita acceso a PyPI y npm. No hacen falta PostgreSQL, cuentas AWS ni Docker. SQLite se utiliza mediante la biblioteca estándar de Python.

## 3. Preparación automática

Desde la raíz del proyecto, en Windows:
```powershell
py --version
node --version
npm --version
py scripts/preparar.py
py scripts/verificar.py
```
En macOS/Linux, reemplazar `py` por `python3`.

El script crea `.venv`, instala las dependencias Python, genera `backend/requirements.lock.txt`, copia configuraciones que no existan y carga seis registros si la base está vacía. En cada frontend usa `npm install` si no existe `package-lock.json`, o `npm ci` si ya existe. No borra archivos de configuración ni registros existentes.

La primera preparación genera los archivos de bloqueo de dependencias. El evaluador debe comprobar instalaciones y builds, y conservar los mismos archivos para todos los candidatos. No cambies versiones durante la prueba.

Las versiones principales se declaran en `package.json` y `requirements.txt`. Dos utilidades Testing Library permiten actualizaciones menores; los locks fijan la resolución completa. No ejecutar `npm audit fix --force` durante la prueba sin revisar el impacto.

## 4. Inicio de servicios

Abre tres terminales independientes en la raíz del proyecto:
```powershell
py scripts/ejecutar.py backend
```
```powershell
py scripts/ejecutar.py vite
```
```powershell
py scripts/ejecutar.py next
```
Detener cada servicio con Ctrl+C en su terminal. El lanzador solo detiene el proceso que inicio y sus hijos.

| Servicio | Dirección | Configuración |
| --- | --- | --- |
| API | `http://127.0.0.1:8000` | `backend/.env` |
| Swagger | `http://127.0.0.1:8000/docs` | Documentación de rutas actuales |
| Vite | `http://127.0.0.1:5173` | `frontend-vite/.env` |
| Next | `http://127.0.0.1:3000/resumen` | `frontend-next/.env.local` |

No ejecutes dos instancias del mismo servicio en el mismo puerto.

## 5. Variables

`DATABASE_PATH` apunta a la base SQLite. Una ruta relativa se interpreta desde `backend/` cuando usas los scripts. `CORS_ORIGINS` contiene orígenes exactos separados por coma. Los valores iniciales permiten localhost y 127.0.0.1 para puertos 5173 y 3000.

`VITE_API_URL` es la URL pública del backend para el navegador. No pongas secretos en variables VITE. `API_URL` se usa desde el servidor Next; no necesita prefijo NEXT_PUBLIC. Reinicia el proceso al cambiar variables. La configuración no es una credencial y los ejemplos solo apuntan al equipo local.

La página Next consulta el backend desde Node; la SPA Vite lo consulta desde el navegador. Por eso un error CORS afecta al acceso desde el navegador y no es un mecanismo de autenticación.

## 6. Pruebas y compilación

Todo lo disponible en el proyecto:
```powershell
py scripts/verificar.py
```
Solo Python, sin presentar el frontend como verificado:
```powershell
py scripts/verificar.py --solo-python
```
Todas las pruebas, pero sin builds:
```powershell
py scripts/verificar.py --sin-build
```
Comandos manuales usando el entorno local desde la raíz:
```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q
cd ..\frontend-vite
npm test
npm run test:logic
npm run build
cd ..\frontend-next
npm test
npm run build
```
Las pruebas Python crean bases temporales. Las pruebas Node de lógica no requieren paquetes externos. Las pruebas de componentes si necesitan las dependencias React/Vitest. Los builds comprueban compilación, no demuestran por si solos el comportamiento funcional. Las pruebas con mocks tampoco sustituyen verificar API y navegador juntos.

## 7. Datos y reinicio seguro

Semilla inicial: 6 pedidos; 3 pendientes, 2 en proceso y 1 completado. `python -m app.seed` no duplica datos si hay registros. No se entrega un comando que borre una base existente.

Para un nuevo candidato, usa una copia nueva del proyecto y una base nueva. Para probar lista vacía, cambia `DATABASE_PATH` a un archivo nuevo como `data/vacia.sqlite3`, reinicia la API y no ejecutes seed. Restaura la configuración al finalizar. Las pruebas automáticas no tocan la base manual.

## 8. Problemas frecuentes

| Problema | Comprobación y acción |
| --- | --- |
| Python o npm no se reconocen | Instalar versiones requeridas, comprobar PATH y abrir una terminal nueva. |
| No se pueden descargar paquetes | Resolver proxy, red corporativa o acceso a repositorios antes del examen. No desactivar TLS. |
| Puerto ocupado | Detener la otra instancia propia o usar otro puerto y ajustar URL/CORS. No terminar procesos ajenos. |
| API funciona pero Vite no carga | Comprobar `VITE_API_URL`, URL exacta de origen y consola/Network del navegador. |
| Next no alcanza la API | Comprobar `API_URL` desde la máquina del servidor Next y reiniciar Next. |
| PATCH devuelve 501 en la base | Es un pendiente intencional P3, no un fallo de instalación. |
| Conteos distintos de la semilla | Se modificaron pedidos; consultar datos actuales o usar una base nueva. |
| Tests React no arrancan | Ejecutar la instalación npm en `frontend-vite` y comprobar la versión de Node. |
| Scripts PowerShell bloqueados | No se necesitan .ps1: usa los scripts Python incluidos. No cambies políticas globales. |

## 9. Git y empaquetado

Antes de comenzar, el evaluador puede crear un repositorio local limpio:
```powershell
git init
git add .
git commit -m "Base de evaluacion"
```
No configurar identidad global del candidato ni hacer push obligatorio. Usar identidad local o un ZIP si la política de la empresa lo prefiere. Los locks deben incluirse; las bases, secretos y dependencias están en .gitignore.

Para entregar:
```powershell
py scripts/empaquetar_entrega.py --salida ../entrega_candidato.zip
```
El script no sobrescribe un ZIP existente. Usa otro nombre para una nueva versión. Siempre revisa su contenido antes de enviarlo; un filtro de archivos no sustituye una revisión de datos sensibles.

## Estado inicial del ejercicio

La API permite crear y consultar pedidos. P1 aún acepta textos en blanco; P2 aún no aplica el filtro; PATCH devuelve 501. Vite lista pedidos sin filtro ni guardado. Next muestra un resumen de ejemplo. Estos son pendientes intencionales de la prueba, no fallos de instalación.

Trabaja en `backend/app/main.py`, `backend/app/repository.py`, `frontend-vite/src/App.jsx` y `frontend-next/app/resumen/page.jsx`, además de las pruebas y plantillas de entrega. No despliegues este ejercicio en producción.

