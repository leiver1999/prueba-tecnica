"""Ejecuta verificaciones; no instala paquetes ni declara exito si falta un paso."""
import argparse
import os
import subprocess
import sys
from common import ROOT, python_exe, node_tools, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solo-python', action='store_true')
    parser.add_argument('--sin-build', action='store_true')
    args = parser.parse_args()
    py = python_exe(require=False)
    run([py, '-m', 'pytest', '-q'], cwd=ROOT / 'backend')
    if args.solo_python:
        print('SOLO PYTHON verificado; frontend no ejecutado.')
        return
    node, npm = node_tools()
    run([node, '--test', 'tests/api.test.mjs'], cwd=ROOT / 'frontend-vite')
    run([node, '--test', 'tests/summary.test.mjs'], cwd=ROOT / 'frontend-next')
    if not (ROOT / 'frontend-vite' / 'node_modules').exists():
        raise RuntimeError('NO VERIFICADO: faltan node_modules para React/Vite. Ejecuta preparar.py.')
    run([npm, 'test'], cwd=ROOT / 'frontend-vite')
    if not args.sin_build:
        env = dict(os.environ, NEXT_TELEMETRY_DISABLED='1')
        run([npm, 'run', 'build'], cwd=ROOT / 'frontend-vite', env=env)
        run([npm, 'run', 'build'], cwd=ROOT / 'frontend-next', env=env)
    print('Verificaciones solicitadas completadas. No sustituyen las pruebas manuales ni la defensa.')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError, OSError) as exc:
        print(f'Verificacion incompleta o fallida: {exc}', file=sys.stderr)
        sys.exit(1)
