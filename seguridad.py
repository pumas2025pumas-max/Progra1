"""Funciones de hashing y verificación de contraseñas."""
from __future__ import annotations

import hashlib


def hash_password(password: str) -> str:
    """Return a SHA-256 hash for the provided *password*."""
    digest = hashlib.sha256()
    digest.update(password.encode("utf-8"))
    return digest.hexdigest()


def verificar_password(password: str, password_hash: str) -> bool:
    """Validate a password against the stored hash."""
    return hash_password(password) == password_hash
