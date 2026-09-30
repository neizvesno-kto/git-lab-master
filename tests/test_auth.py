"""
Тесты для модуля аутентификации (src/auth).
"""

import pytest
from src.auth.login import hash_password, verify_password, login
from src.auth.register import validate_email, validate_password, register


# ──────────────────────────── login.py ────────────────────────────

class TestHashPassword:
    def test_same_input_same_hash(self):
        assert hash_password("Pass1234", "salt") == hash_password("Pass1234", "salt")

    def test_different_salt_different_hash(self):
        assert hash_password("Pass1234", "salt1") != hash_password("Pass1234", "salt2")


class TestVerifyPassword:
    def test_correct_password(self):
        h = hash_password("Secret1!", "mysalt")
        assert verify_password("Secret1!", "mysalt", h) is True

    def test_wrong_password(self):
        h = hash_password("Secret1!", "mysalt")
        assert verify_password("wrong", "mysalt", h) is False


class TestLogin:
    def setup_method(self):
        self.db = {}
        from src.auth.register import register
        register("alice", "alice@example.com", "Password1", self.db)

    def test_valid_login(self):
        result = login("alice", "Password1", self.db)
        assert result is not None
        assert result["username"] == "alice"

    def test_wrong_password(self):
        assert login("alice", "wrong", self.db) is None

    def test_unknown_user(self):
        assert login("bob", "Password1", self.db) is None


# ──────────────────────────── register.py ────────────────────────────

class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_invalid_email(self):
        assert validate_email("not-an-email") is False


class TestValidatePassword:
    def test_too_short(self):
        ok, _ = validate_password("Ab1")
        assert ok is False

    def test_no_uppercase(self):
        ok, _ = validate_password("password1")
        assert ok is False

    def test_no_digit(self):
        ok, _ = validate_password("Password")
        assert ok is False

    def test_valid_password(self):
        ok, _ = validate_password("Password1")
        assert ok is True


class TestRegister:
    def setup_method(self):
        self.db = {}

    def test_successful_registration(self):
        rec = register("bob", "bob@example.com", "Password1", self.db)
        assert rec["username"] == "bob"
        assert "bob" in self.db

    def test_duplicate_user(self):
        register("bob", "bob@example.com", "Password1", self.db)
        with pytest.raises(ValueError, match="уже существует"):
            register("bob", "bob2@example.com", "Password1", self.db)

    def test_invalid_email(self):
        with pytest.raises(ValueError, match="email"):
            register("carol", "bad-email", "Password1", self.db)
