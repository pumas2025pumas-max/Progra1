"""Gestión de usuarios de la aplicación Kiwillet."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from io_archivos import escribir_json, leer_json, ruta_datos
from logger import registrar_evento
from seguridad import hash_password, verificar_password

USUARIOS_PATH = ruta_datos("usuarios.json")


@dataclass
class Usuario:
    nombre: str
    password_hash: str
    saldo: float = 0.0

    def to_dict(self) -> Dict[str, str | float]:
        return {
            "usuario": self.nombre,
            "password_hash": self.password_hash,
            "saldo": self.saldo,
        }


def cargar_usuarios() -> Dict[str, Usuario]:
    datos = leer_json(USUARIOS_PATH, default=[])
    usuarios: Dict[str, Usuario] = {}
    for entrada in datos:
        nombre = entrada.get("usuario", "")
        if not nombre:
            continue
        usuarios[nombre] = Usuario(
            nombre=nombre,
            password_hash=entrada.get("password_hash", ""),
            saldo=float(entrada.get("saldo", 0.0)),
        )
    return usuarios


def guardar_usuarios(usuarios: Dict[str, Usuario]) -> None:
    escribir_json(USUARIOS_PATH, [usuario.to_dict() for usuario in usuarios.values()])


def crear_usuario(usuarios: Dict[str, Usuario], nombre: str, password: str) -> bool:
    if nombre in usuarios:
        return False
    usuario = Usuario(nombre=nombre, password_hash=hash_password(password), saldo=0.0)
    usuarios[nombre] = usuario
    guardar_usuarios(usuarios)
    registrar_evento("alta_usuario", nombre)
    return True


def autenticar_usuario(usuarios: Dict[str, Usuario], nombre: str, password: str) -> Optional[Usuario]:
    usuario = usuarios.get(nombre)
    if usuario is None:
        registrar_evento("login_fallido", nombre)
        return None
    if verificar_password(password, usuario.password_hash):
        registrar_evento("login_exitoso", nombre)
        return usuario
    registrar_evento("login_fallido", nombre)
    return None


def cambiar_contrasena(usuarios: Dict[str, Usuario], nombre: str, nueva_password: str) -> bool:
    usuario = usuarios.get(nombre)
    if usuario is None:
        return False
    usuario.password_hash = hash_password(nueva_password)
    guardar_usuarios(usuarios)
    registrar_evento("cambio_password", nombre)
    return True


def actualizar_saldo(usuarios: Dict[str, Usuario], nombre: str, saldo: float) -> None:
    usuario = usuarios.get(nombre)
    if usuario is None:
        return
    usuario.saldo = saldo
    guardar_usuarios(usuarios)
