"""Genera un ZIP sin entornos, dependencias, datos locales, secretos ni .git."""
import argparse
from pathlib import Path
import zipfile
from common import ROOT

EXCLUDED_DIRS = {'.venv', 'node_modules', '.next', 'dist', '__pycache__', '.pytest_cache', '.git', '.vitest', 'coverage'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', default=str(ROOT.parent / 'entrega_candidato.zip'))
    args = parser.parse_args()
    destination = Path(args.salida).resolve()
    if destination.exists():
        raise SystemExit(f'El archivo ya existe: {destination}. Usa otro nombre; no se sobrescribe.')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob('*')):
            if not path.is_file() or path.is_symlink() or path.resolve() == destination:
                continue
            rel = path.relative_to(ROOT)
            if any(part in EXCLUDED_DIRS for part in rel.parts):
                continue
            if path.name.startswith('.env') and path.name != '.env.example':
                continue
            if path.suffix in {'.pyc', '.log', '.zip', '.sqlite3'} or '.sqlite3-' in path.name:
                continue
            archive.write(path, Path('entrega') / rel)
    print(f'Entrega creada: {destination}')
    print('Revisa manualmente que no incluya informacion privada antes de enviarla.')


if __name__ == '__main__':
    main()
