"""Manejo del catálogo de servicios a pagar."""
from __future__ import annotations

from typing import Dict, List, Optional

from io_archivos import escribir_csv, leer_csv, ruta_datos

CAMPOS_SERVICIO = ["id", "nombre", "categoria", "monto"]
SERVICIOS_PATH = ruta_datos("servicios.csv")
SERVICIOS_BASE = [
    {"id": "1", "nombre": "Luz", "categoria": "Hogar", "monto": "4500"},
    {"id": "2", "nombre": "Agua", "categoria": "Hogar", "monto": "3000"},
    {"id": "3", "nombre": "Gas", "categoria": "Hogar", "monto": "2500"},
    {"id": "4", "nombre": "Internet", "categoria": "Comunicación", "monto": "6500"},
    {"id": "5", "nombre": "Telefonía", "categoria": "Comunicación", "monto": "2200"},
]


def inicializar_catalogo() -> None:
    if not SERVICIOS_PATH.exists():
        escribir_csv(SERVICIOS_PATH, CAMPOS_SERVICIO, SERVICIOS_BASE)


def cargar_servicios() -> List[Dict[str, str]]:
    inicializar_catalogo()
    return leer_csv(SERVICIOS_PATH)


def obtener_servicio(servicios: List[Dict[str, str]], servicio_id: str) -> Optional[Dict[str, str]]:
    return next((servicio for servicio in servicios if servicio.get("id") == servicio_id), None)
