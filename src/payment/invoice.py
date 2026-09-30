"""
Модуль формирования счетов (инвойсов).
Генерирует счёт на основе платёжной транзакции.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
from typing import List
import uuid


@dataclass
class InvoiceItem:
    description: str
    quantity: int
    unit_price: Decimal

    @property
    def total(self) -> Decimal:
        return Decimal(self.quantity) * self.unit_price


@dataclass
class Invoice:
    user_id: str
    items: List[InvoiceItem] = field(default_factory=list)
    invoice_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    paid: bool = False

    def add_item(self, description: str, quantity: int, unit_price: Decimal) -> None:
        self.items.append(InvoiceItem(description, quantity, unit_price))

    @property
    def subtotal(self) -> Decimal:
        return sum(item.total for item in self.items)

    @property
    def tax(self) -> Decimal:
        """НДС 20%."""
        return (self.subtotal * Decimal("0.20")).quantize(Decimal("0.01"))

    @property
    def total(self) -> Decimal:
        return self.subtotal + self.tax

    def mark_paid(self) -> None:
        self.paid = True

    def to_dict(self) -> dict:
        return {
            "invoice_id": self.invoice_id,
            "user_id": self.user_id,
            "items": [
                {
                    "description": i.description,
                    "quantity": i.quantity,
                    "unit_price": str(i.unit_price),
                    "total": str(i.total),
                }
                for i in self.items
            ],
            "subtotal": str(self.subtotal),
            "tax": str(self.tax),
            "total": str(self.total),
            "paid": self.paid,
        }
