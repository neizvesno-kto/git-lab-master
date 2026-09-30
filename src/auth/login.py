"""
Модуль аутентификации пользователей.
Обеспечивает вход в систему по логину и паролю.
"""

import hashlib
import hmac
from typing import Optional


def hash_password(password: str, salt: str) -> str:
    """Хэширует пароль с солью через PBKDF2-HMAC-SHA256."""
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations=100_000,
    )
    return dk.hex()


def verify_password(password: str, salt: str, hashed: str) -> bool:
    """Проверяет соответствие пароля его хэшу."""
    return hmac.compare_digest(hash_password(password, salt), hashed)


def login(username: str, password: str, user_db: dict) -> Optional[dict]:
    """
    Выполняет вход пользователя.

    Args:
        username: имя пользователя
        password: пароль в открытом виде
        user_db: словарь пользователей {username: {salt, password_hash, ...}}

    Returns:
        Словарь с данными пользователя при успехе, None при неудаче.
    """
    user = user_db.get(username)
    if user is None:
        return None
    if verify_password(password, user["salt"], user["password_hash"]):
        return {"username": username, "email": user.get("email")}
    return None
