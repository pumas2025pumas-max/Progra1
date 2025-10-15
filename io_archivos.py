"""Utility functions for reading and writing project data files."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"


def asegurar_estructura_directorios() -> None:
    """Ensure the expected directory structure exists."""
    for folder in (DATA_DIR, LOG_DIR, REPORTS_DIR):
        folder.mkdir(parents=True, exist_ok=True)


def ruta_datos(nombre_archivo: str) -> Path:
    """Return the absolute path for a data file located inside DATA_DIR."""
    asegurar_estructura_directorios()
    return DATA_DIR / nombre_archivo


def ruta_log(nombre_archivo: str) -> Path:
    """Return the absolute path for a log file located inside LOG_DIR."""
    asegurar_estructura_directorios()
    return LOG_DIR / nombre_archivo


def ruta_reporte(nombre_archivo: str) -> Path:
    """Return the absolute path for a report file located inside REPORTS_DIR."""
    asegurar_estructura_directorios()
    return REPORTS_DIR / nombre_archivo


def leer_json(path: Path, default: Any) -> Any:
    """Read JSON data from *path* returning *default* if the file does not exist."""
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return default


def escribir_json(path: Path, data: Any) -> None:
    """Write *data* as JSON into *path*."""
    with path.open("w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=2, ensure_ascii=False)


def leer_csv(path: Path, fieldnames: Iterable[str] | None = None) -> List[Dict[str, str]]:
    """Read a CSV file returning a list of dictionaries."""
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo) if fieldnames is None else csv.DictReader(archivo, fieldnames=fieldnames)
        return [dict(fila) for fila in lector]


def escribir_csv(path: Path, fieldnames: Iterable[str], rows: Iterable[Dict[str, Any]]) -> None:
    """Write dictionaries in *rows* to *path* as CSV using the given *fieldnames*."""
    with path.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=fieldnames)
        escritor.writeheader()
        for fila in rows:
            escritor.writerow({clave: fila.get(clave, "") for clave in fieldnames})
