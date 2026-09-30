"""
Тесты для модуля платежей (src/payment).
"""

import pytest
from decimal import Decimal
from src.payment.payment import Payment, PaymentService, PaymentStatus
from src.payment.invoice import Invoice, InvoiceItem


class TestPayment:
    def test_create_payment(self):
        p = Payment("user1", Decimal("100.00"))
        assert p.status == PaymentStatus.PENDING
        assert p.amount == Decimal("100.00")

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError):
            Payment("user1", Decimal("-10"))

    def test_confirm(self):
        p = Payment("user1", Decimal("50"))
        p.confirm()
        assert p.status == PaymentStatus.CONFIRMED

    def test_refund_after_confirm(self):
        p = Payment("user1", Decimal("50"))
        p.confirm()
        p.refund()
        assert p.status == PaymentStatus.REFUNDED

    def test_refund_without_confirm_raises(self):
        p = Payment("user1", Decimal("50"))
        with pytest.raises(RuntimeError):
            p.refund()


class TestPaymentService:
    def setup_method(self):
        self.svc = PaymentService()

    def test_create_and_get(self):
        p = self.svc.create_payment("user1", Decimal("200"))
        found = self.svc.get_payment(p.payment_id)
        assert found is p

    def test_confirm_payment(self):
        p = self.svc.create_payment("user1", Decimal("200"))
        self.svc.confirm_payment(p.payment_id)
        assert p.status == PaymentStatus.CONFIRMED

    def test_missing_payment_raises(self):
        with pytest.raises(KeyError):
            self.svc.confirm_payment("nonexistent-id")


class TestInvoice:
    def test_totals(self):
        inv = Invoice(user_id="user1")
        inv.add_item("Товар A", 2, Decimal("100.00"))
        assert inv.subtotal == Decimal("200.00")
        assert inv.tax == Decimal("40.00")
        assert inv.total == Decimal("240.00")

    def test_mark_paid(self):
        inv = Invoice(user_id="user1")
        inv.mark_paid()
        assert inv.paid is True
