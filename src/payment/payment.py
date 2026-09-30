"""
Модуль обработки платежей.
Поддерживает создание, подтверждение и отмену транзакций.
"""

from decimal import Decimal
from enum import Enum
from typing import Optional
import uuid
from datetime import datetime


class PaymentStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment:
    """Представляет одну платёжную транзакцию."""

    def __init__(self, user_id: str, amount: Decimal, currency: str = "RUB"):
        if amount <= 0:
            raise ValueError("Сумма платежа должна быть положительной")
        self.payment_id: str = str(uuid.uuid4())
        self.user_id: str = user_id
        self.amount: Decimal = amount
        self.currency: str = currency
        self.status: PaymentStatus = PaymentStatus.PENDING
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = self.created_at

    def confirm(self) -> None:
        """Подтверждает платёж."""
        if self.status != PaymentStatus.PENDING:
            raise RuntimeError(f"Нельзя подтвердить платёж со статусом {self.status}")
        self.status = PaymentStatus.CONFIRMED
        self.updated_at = datetime.utcnow()

    def fail(self, reason: str = "") -> None:
        """Отмечает платёж как неуспешный."""
        if self.status != PaymentStatus.PENDING:
            raise RuntimeError(f"Нельзя отклонить платёж со статусом {self.status}")
        self.status = PaymentStatus.FAILED
        self.updated_at = datetime.utcnow()

    def refund(self) -> None:
        """Выполняет возврат средств."""
        if self.status != PaymentStatus.CONFIRMED:
            raise RuntimeError("Возврат возможен только для подтверждённых платежей")
        self.status = PaymentStatus.REFUNDED
        self.updated_at = datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "user_id": self.user_id,
            "amount": str(self.amount),
            "currency": self.currency,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }


class PaymentService:
    """Сервис управления платежами."""

    def __init__(self):
        self._payments: dict[str, Payment] = {}

    def create_payment(self, user_id: str, amount: Decimal, currency: str = "RUB") -> Payment:
        p = Payment(user_id, amount, currency)
        self._payments[p.payment_id] = p
        return p

    def get_payment(self, payment_id: str) -> Optional[Payment]:
        return self._payments.get(payment_id)

    def confirm_payment(self, payment_id: str) -> Payment:
        p = self._get_or_raise(payment_id)
        p.confirm()
        return p

    def refund_payment(self, payment_id: str) -> Payment:
        p = self._get_or_raise(payment_id)
        p.refund()
        return p

    def _get_or_raise(self, payment_id: str) -> Payment:
        p = self._payments.get(payment_id)
        if p is None:
            raise KeyError(f"Платёж {payment_id} не найден")
        return p
