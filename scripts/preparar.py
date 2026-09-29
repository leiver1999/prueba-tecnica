"""Preparacion previa a la prueba. No borra datos ni modifica instalaciones globales."""
import argparse
import shutil
import subprocess
import sys
import venv
from common import ROOT, VENV, python_exe, node_tools, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solo-python', action='store_true')
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        raise RuntimeError('Se requiere Python 3.11 o superior; se recomienda 3.12/3.13.')
    if not args.solo_python:
        _, npm = node_tools()
    if not VENV.exists():
        print('Creando entorno virtual local...')
        venv.EnvBuilder(with_pip=True).create(VENV)
    py = python_exe()
    backend = ROOT / 'backend'
    lock = backend / 'requirements.lock.txt'
    source = lock if lock.exists() else backend / 'requirements.txt'
    run([py, '-m', 'pip', 'install', '-r', source])
    if not lock.exists():
        frozen = subprocess.check_output([py, '-m', 'pip', 'freeze'], text=True)
        lock.write_text(frozen, encoding='utf-8')
    for folder, destination in [('backend', '.env'), ('frontend-vite', '.env'), ('frontend-next', '.env.local')]:
        path = ROOT / folder / destination
        if not path.exists():
            shutil.copy2(ROOT / folder / '.env.example', path)
    # Seed respeta DATABASE_PATH de backend/.env, igual que uvicorn --env-file.
    run([py, '-c', "from dotenv import load_dotenv; load_dotenv('.env'); from app.seed import main; main()"], cwd=backend)
    if not args.solo_python:
        for folder in ['frontend-vite', 'frontend-next']:
            project = ROOT / folder
            action = 'ci' if (project / 'package-lock.json').exists() else 'install'
            run([npm, action], cwd=project)
    print('Preparacion terminada. Ejecuta python scripts/verificar.py antes de la sesion.')
    print('Conserva requirements.lock.txt y ambos package-lock.json para todos los candidatos.')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError, OSError) as exc:
        print(f'No se completo la preparacion: {exc}', file=sys.stderr)
        sys.exit(1)
