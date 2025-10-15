"""Funciones de apoyo para el programa de la billetera."""

import os

USUARIOS_ARCHIVO = "usuarios.txt"
TARJETAS_ARCHIVO = "tarjetas.txt"
MOVIMIENTOS_ARCHIVO = "movimientos.txt"
SERVICIOS_ARCHIVO = "servicios.txt"

# ---------------- Archivos ----------------

def inicializar_archivos():
    if not os.path.exists(USUARIOS_ARCHIVO):
        open(USUARIOS_ARCHIVO, "w", encoding="utf-8").close()
    if not os.path.exists(TARJETAS_ARCHIVO):
        open(TARJETAS_ARCHIVO, "w", encoding="utf-8").close()
    if not os.path.exists(MOVIMIENTOS_ARCHIVO):
        open(MOVIMIENTOS_ARCHIVO, "w", encoding="utf-8").close()
    if not os.path.exists(SERVICIOS_ARCHIVO):
        with open(SERVICIOS_ARCHIVO, "w", encoding="utf-8") as archivo:
            archivo.write("agu;Agua corriente;1800\n")
            archivo.write("ele;Electricidad;2500\n")
            archivo.write("int;Internet;3200\n")


# ---------------- Usuarios ----------------

def leer_usuarios():
    usuarios = {}
    if not os.path.exists(USUARIOS_ARCHIVO):
        return usuarios
    with open(USUARIOS_ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(";")
            if len(partes) < 3:
                continue
            nombre = partes[0]
            clave = partes[1]
            try:
                saldo = float(partes[2])
            except ValueError:
                saldo = 0.0
            usuarios[nombre] = {"clave": clave, "saldo": saldo}
    return usuarios


def guardar_usuarios(usuarios):
    with open(USUARIOS_ARCHIVO, "w", encoding="utf-8") as archivo:
        for nombre, datos in usuarios.items():
            linea = f"{nombre};{datos['clave']};{datos['saldo']}\n"
            archivo.write(linea)


# ---------------- Tarjetas ----------------

def leer_tarjetas():
    tarjetas = {}
    if not os.path.exists(TARJETAS_ARCHIVO):
        return tarjetas
    with open(TARJETAS_ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(";")
            if len(partes) < 5:
                continue
            usuario, alias, numero, tipo, vencimiento = partes[:5]
            tarjetas.setdefault(usuario, []).append(
                {
                    "alias": alias,
                    "numero": numero,
                    "tipo": tipo,
                    "vencimiento": vencimiento,
                }
            )
    return tarjetas


def guardar_tarjetas(tarjetas):
    with open(TARJETAS_ARCHIVO, "w", encoding="utf-8") as archivo:
        for usuario, lista in tarjetas.items():
            for tarjeta in lista:
                linea = "{};{};{};{};{}\n".format(
                    usuario,
                    tarjeta.get("alias", ""),
                    tarjeta.get("numero", ""),
                    tarjeta.get("tipo", ""),
                    tarjeta.get("vencimiento", ""),
                )
                archivo.write(linea)


def obtener_tarjetas_usuario(tarjetas, usuario):
    return tarjetas.get(usuario, [])


def agregar_tarjeta(tarjetas, usuario, alias, numero, tipo, vencimiento):
    lista = tarjetas.setdefault(usuario, [])
    for tarjeta in lista:
        if tarjeta.get("alias") == alias:
            return False
    lista.append(
        {
            "alias": alias,
            "numero": numero,
            "tipo": tipo,
            "vencimiento": vencimiento,
        }
    )
    guardar_tarjetas(tarjetas)
    return True


def eliminar_tarjeta(tarjetas, usuario, alias):
    lista = tarjetas.get(usuario, [])
    nueva_lista = [tarjeta for tarjeta in lista if tarjeta.get("alias") != alias]
    if len(nueva_lista) == len(lista):
        return False
    tarjetas[usuario] = nueva_lista
    guardar_tarjetas(tarjetas)
    return True


def mascara_tarjeta(numero):
    numero = numero.strip()
    if len(numero) >= 4:
        return "****" + numero[-4:]
    return numero


# ---------------- Movimientos ----------------

def leer_movimientos():
    movimientos = {}
    if not os.path.exists(MOVIMIENTOS_ARCHIVO):
        return movimientos
    with open(MOVIMIENTOS_ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(";")
            if len(partes) < 5:
                continue
            usuario, fecha, concepto, monto, saldo = partes[:5]
            movimientos.setdefault(usuario, []).append(
                {
                    "fecha": fecha,
                    "concepto": concepto,
                    "monto": monto,
                    "saldo": saldo,
                }
            )
    return movimientos


def guardar_movimientos(movimientos):
    with open(MOVIMIENTOS_ARCHIVO, "w", encoding="utf-8") as archivo:
        for usuario, lista in movimientos.items():
            for movimiento in lista:
                linea = "{};{};{};{};{}\n".format(
                    usuario,
                    movimiento.get("fecha", ""),
                    movimiento.get("concepto", ""),
                    movimiento.get("monto", ""),
                    movimiento.get("saldo", ""),
                )
                archivo.write(linea)


def registrar_movimiento(movimientos, usuario, fecha, concepto, monto, saldo):
    movimientos.setdefault(usuario, []).append(
        {
            "fecha": fecha,
            "concepto": concepto,
            "monto": monto,
            "saldo": saldo,
        }
    )
    guardar_movimientos(movimientos)


# ---------------- Servicios ----------------

def leer_servicios():
    servicios = []
    if not os.path.exists(SERVICIOS_ARCHIVO):
        return servicios
    with open(SERVICIOS_ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(";")
            if len(partes) < 3:
                continue
            servicios.append(
                {
                    "codigo": partes[0],
                    "nombre": partes[1],
                    "monto": partes[2],
                }
            )
    return servicios


def buscar_servicio(servicios, codigo):
    for servicio in servicios:
        if servicio.get("codigo") == codigo:
            return servicio
    return None


# ---------------- Utilidades ----------------

def formatear_monto(valor):
    try:
        numero = float(valor)
    except ValueError:
        numero = 0.0
    return f"${numero:.2f}"
