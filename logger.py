"""Simple file logger for the Kiwillet application."""
from __future__ import annotations

from datetime import datetime

from io_archivos import ruta_log


BITACORA = ruta_log("bitacora.log")


def registrar_evento(accion: str, detalle: str = "") -> None:
    """Append a log entry with current timestamp, action and detail."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with BITACORA.open("a", encoding="utf-8") as archivo:
        archivo.write(f"{timestamp};{accion};{detalle}\n")
