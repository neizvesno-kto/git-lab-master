# API Reference

## Модуль `src.auth`

### `login(username, password, user_db) → dict | None`

Аутентифицирует пользователя.

**Параметры:**
| Параметр | Тип | Описание |
|----------|-----|---------|
| `username` | `str` | Имя пользователя |
| `password` | `str` | Пароль в открытом виде |
| `user_db` | `dict` | Хранилище пользователей |

**Возвращает:** `{"username": ..., "email": ...}` при успехе, `None` при неудаче.

---

### `register(username, email, password, user_db) → dict`

Регистрирует нового пользователя.

**Параметры:**
| Параметр | Тип | Описание |
|----------|-----|---------|
| `username` | `str` | Желаемое имя пользователя |
| `email` | `str` | Email адрес |
| `password` | `str` | Пароль (мин. 8 символов, 1 заглавная, 1 цифра) |
| `user_db` | `dict` | Изменяемое хранилище пользователей |

**Возвращает:** словарь с данными пользователя.

**Исключения:**
- `ValueError` — пользователь уже существует, некорректный email или слабый пароль.

---

## Модуль `src.payment`

### Класс `PaymentService`

#### `create_payment(user_id, amount, currency="RUB") → Payment`

Создаёт новую транзакцию со статусом `PENDING`.

#### `confirm_payment(payment_id) → Payment`

Подтверждает платёж. Переводит статус в `CONFIRMED`.

**Исключения:** `KeyError` если платёж не найден, `RuntimeError` если статус не `PENDING`.

#### `refund_payment(payment_id) → Payment`

Выполняет возврат. Переводит статус в `REFUNDED`.

**Исключения:** `RuntimeError` если статус не `CONFIRMED`.

---

### Класс `Invoice`

#### `add_item(description, quantity, unit_price) → None`

Добавляет позицию в счёт.

#### `total → Decimal`

Итоговая сумма с НДС 20%.

#### `mark_paid() → None`

Отмечает счёт как оплаченный.

#### `to_dict() → dict`

Сериализует счёт в словарь.

---

## Примеры использования

### Регистрация и вход

```python
from src.auth import register, login

db = {}
register("alice", "alice@example.com", "Password1", db)
user = login("alice", "Password1", db)
print(user)  # {'username': 'alice', 'email': 'alice@example.com'}
```

### Создание и подтверждение платежа

```python
from decimal import Decimal
from src.payment import PaymentService

svc = PaymentService()
p = svc.create_payment("alice", Decimal("500.00"))
svc.confirm_payment(p.payment_id)
print(p.status)  # PaymentStatus.CONFIRMED
```

---

> **���������:** �� �������� ����� ���������� ��� Decimal ��� ������ ����������. � ����������� loat ��� ���������� ��������.
