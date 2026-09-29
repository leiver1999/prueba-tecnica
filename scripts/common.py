from pathlib import Path
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / '.venv'


def python_exe(require=True):
    path = VENV / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if path.exists():
        return str(path)
    if not require:
        return sys.executable
    raise RuntimeError('Primero ejecuta: python scripts/preparar.py')


def node_tools():
    node = shutil.which('node')
    npm = shutil.which('npm.cmd' if os.name == 'nt' else 'npm')
    if not node or not npm:
        raise RuntimeError('Instala Node.js 22.12+ (rama 22 o 24) con npm y abre otra terminal.')
    version = subprocess.check_output([node, '--version'], text=True).strip()
    nums = tuple(int(x) for x in version.lstrip('v').split('.')[:3])
    if nums < (22, 12, 0):
        raise RuntimeError(f'Node insuficiente: {version}. Se requiere 22.12 o superior.')
    return node, npm


def run(args, cwd=ROOT, **kwargs):
    print('>', ' '.join(str(x) for x in args), flush=True)
    return subprocess.run([str(x) for x in args], cwd=cwd, check=True, **kwargs)
