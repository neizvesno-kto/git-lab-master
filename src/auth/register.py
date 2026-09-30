"""
Модуль регистрации новых пользователей.
Валидирует входные данные и создаёт запись в базе пользователей.
"""

import os
import re
from typing import Tuple

from .login import hash_password


EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$", re.IGNORECASE)
MIN_PASSWORD_LEN = 8


def validate_email(email: str) -> bool:
    """Проверяет корректность формата email."""
    return bool(EMAIL_RE.match(email))


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Проверяет надёжность пароля.

    Returns:
        (True, "") если пароль подходит, иначе (False, причина).
    """
    if len(password) < MIN_PASSWORD_LEN:
        return False, f"Пароль должен содержать минимум {MIN_PASSWORD_LEN} символов"
    if not re.search(r"[A-Z]", password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву"
    if not re.search(r"\d", password):
        return False, "Пароль должен содержать хотя бы одну цифру"
    return True, ""


def register(username: str, email: str, password: str, user_db: dict) -> dict:
    """
    Регистрирует нового пользователя.

    Args:
        username: желаемое имя пользователя
        email: адрес электронной почты
        password: пароль в открытом виде
        user_db: изменяемый словарь пользователей

    Returns:
        Созданную запись пользователя.

    Raises:
        ValueError: если данные не прошли валидацию или пользователь уже существует.
    """
    if username in user_db:
        raise ValueError(f"Пользователь '{username}' уже существует")
    if not validate_email(email):
        raise ValueError(f"Некорректный email: {email}")
    ok, reason = validate_password(password)
    if not ok:
        raise ValueError(reason)

    salt = os.urandom(16).hex()
    password_hash = hash_password(password, salt)

    user_record = {
        "username": username,
        "email": email,
        "salt": salt,
        "password_hash": password_hash,
    }
    user_db[username] = user_record
    return user_record
