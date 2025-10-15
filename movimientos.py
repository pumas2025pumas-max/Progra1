"""Registro de movimientos y generación de reportes estadísticos."""
from __future__ import annotations

from collections import Counter
from datetime import datetime
from statistics import mean
from typing import Dict, Iterable, List

from io_archivos import escribir_csv, leer_csv, ruta_datos, ruta_reporte
from logger import registrar_evento

CAMPOS_MOVIMIENTO = ["fecha", "tipo", "descripcion", "monto", "saldo_resultante"]


def _ruta_movimientos(usuario: str):
    return ruta_datos(f"movimientos_{usuario}.csv")


def cargar_movimientos(usuario: str) -> List[Dict[str, str]]:
    return leer_csv(_ruta_movimientos(usuario))


def guardar_movimientos(usuario: str, movimientos: List[Dict[str, str]]) -> None:
    escribir_csv(_ruta_movimientos(usuario), CAMPOS_MOVIMIENTO, movimientos)


def registrar_movimiento(
    usuario: str,
    movimientos: List[Dict[str, str]],
    tipo: str,
    descripcion: str,
    monto: float,
    saldo_resultante: float,
) -> None:
    entrada = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo,
        "descripcion": descripcion,
        "monto": f"{monto:.2f}",
        "saldo_resultante": f"{saldo_resultante:.2f}",
    }
    movimientos.append(entrada)
    guardar_movimientos(usuario, movimientos)
    registrar_evento("movimiento", f"{usuario}:{tipo}:{monto:.2f}")


def _valores_float(movimientos: Iterable[Dict[str, str]], campo: str) -> List[float]:
    valores: List[float] = []
    for movimiento in movimientos:
        try:
            valores.append(float(movimiento.get(campo, 0) or 0))
        except ValueError:
            continue
    return valores


def calcular_estadisticas(movimientos: List[Dict[str, str]]) -> Dict[str, float | str]:
    if not movimientos:
        return {
            "saldo_promedio": 0.0,
            "total_ingresos": 0.0,
            "total_gastos": 0.0,
            "servicio_mas_pagado": "N/A",
        }

    saldos = _valores_float(movimientos, "saldo_resultante")
    montos = _valores_float(movimientos, "monto")
    tipos = [movimiento.get("tipo", "") for movimiento in movimientos]
    descripciones = [movimiento.get("descripcion", "") for movimiento in movimientos if "servicio" in movimiento.get("tipo", "").lower()]

    total_ingresos = sum(monto for monto, tipo in zip(montos, tipos) if "ingreso" in tipo.lower() or "recarga" in tipo.lower())
    total_gastos = sum(monto for monto, tipo in zip(montos, tipos) if "pago" in tipo.lower())
    mas_pagado = "N/A"
    if descripciones:
        contador = Counter(descripciones)
        mas_pagado = max(contador.items(), key=lambda par: par[1])[0]

    return {
        "saldo_promedio": mean(saldos) if saldos else 0.0,
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "servicio_mas_pagado": mas_pagado,
    }


def generar_reporte(usuario: str, movimientos: List[Dict[str, str]]) -> str:
    estadisticas = calcular_estadisticas(movimientos)
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = ruta_reporte(f"reporte_{usuario}_{fecha}.csv")
    filas: List[Dict[str, str]] = [
        {"metrica": "Saldo promedio", "valor": f"{estadisticas['saldo_promedio']:.2f}"},
        {"metrica": "Total ingresos", "valor": f"{estadisticas['total_ingresos']:.2f}"},
        {"metrica": "Total gastos", "valor": f"{estadisticas['total_gastos']:.2f}"},
        {"metrica": "Servicio más pagado", "valor": estadisticas["servicio_mas_pagado"]},
    ]
    escribir_csv(ruta, ["metrica", "valor"], filas)
    registrar_evento("reporte_generado", f"{usuario}:{ruta.name}")
    return str(ruta)
