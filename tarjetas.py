"""Funciones para administrar tarjetas asociadas a un usuario."""
from __future__ import annotations

from typing import Dict, List, Optional

from io_archivos import escribir_csv, leer_csv, ruta_datos
from logger import registrar_evento

CAMPOS_TARJETA = ["id", "tipo", "entidad", "numero", "vencimiento"]


def _ruta_tarjetas(usuario: str):
    return ruta_datos(f"tarjetas_{usuario}.csv")


def cargar_tarjetas(usuario: str) -> List[Dict[str, str]]:
    return leer_csv(_ruta_tarjetas(usuario))


def guardar_tarjetas(usuario: str, tarjetas: List[Dict[str, str]]) -> None:
    escribir_csv(_ruta_tarjetas(usuario), CAMPOS_TARJETA, tarjetas)


def agregar_tarjeta(usuario: str, tarjetas: List[Dict[str, str]], tarjeta: Dict[str, str]) -> bool:
    if any(t.get("id") == tarjeta.get("id") for t in tarjetas):
        return False
    tarjetas.append({campo: tarjeta.get(campo, "") for campo in CAMPOS_TARJETA})
    guardar_tarjetas(usuario, tarjetas)
    registrar_evento("alta_tarjeta", f"{usuario}:{tarjeta.get('id','')}")
    return True


def eliminar_tarjeta(usuario: str, tarjetas: List[Dict[str, str]], tarjeta_id: str) -> bool:
    indice = next((i for i, tarjeta in enumerate(tarjetas) if tarjeta.get("id") == tarjeta_id), None)
    if indice is None:
        return False
    tarjetas.pop(indice)
    guardar_tarjetas(usuario, tarjetas)
    registrar_evento("baja_tarjeta", f"{usuario}:{tarjeta_id}")
    return True


def obtener_tarjeta(tarjetas: List[Dict[str, str]], tarjeta_id: str) -> Optional[Dict[str, str]]:
    return next((tarjeta for tarjeta in tarjetas if tarjeta.get("id") == tarjeta_id), None)
