"""Usar una terminal por servicio: backend, vite o next. Ctrl+C para detenerlo."""
import argparse
import os
import signal
import subprocess
import sys
from common import ROOT, python_exe, node_tools


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('servicio', choices=['backend', 'vite', 'next'])
    args = parser.parse_args()
    if args.servicio == 'backend':
        cwd = ROOT / 'backend'
        command = [python_exe(), '-m', 'uvicorn', 'app.main:app', '--reload', '--host', '127.0.0.1', '--port', '8000']
        if (cwd / '.env').exists():
            command += ['--env-file', '.env']
    else:
        _, npm = node_tools()
        cwd = ROOT / ('frontend-vite' if args.servicio == 'vite' else 'frontend-next')
        if not (cwd / 'node_modules').is_dir():
            raise RuntimeError('Faltan dependencias. Ejecuta primero scripts/preparar.py.')
        command = [npm, 'run', 'dev']
    env = dict(os.environ, NEXT_TELEMETRY_DISABLED='1')
    print('Servicio local:', args.servicio, '| Ctrl+C para detener.', flush=True)
    process = subprocess.Popen(command, cwd=cwd, env=env)
    try:
        return process.wait()
    except KeyboardInterrupt:
        # Solo se detiene el proceso creado aqui y sus hijos, nunca procesos ajenos.
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            process.send_signal(signal.SIGINT)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.terminate()
        return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
