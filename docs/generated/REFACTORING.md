# Refactoring Suggestions

12 suggestions.

## 1. Replace Nested Conditionals with Guard Clauses

- **Location**: `sample-project/ecommerce/order_service.py:17 · OrderService.place_order`
- **Why**: Nesting reaches depth 7. Invert conditions and return early to flatten the body.

**Before**

```python
def process(user, order):
    if user is not None:
        if order is not None:
            if order.paid:
                if user.active:
                    ship(order)

```

**After**

```python
def process(user, order):
    if user is None or order is None:
        return None
    if not order.paid:
        return None
    if not user.active:
        return None
    ship(order)

```

---

## 2. Handle or Propagate the Exception

- **Location**: `sample-project/ecommerce/order_service.py:17 · OrderService.place_order`
- **Why**: An exception is caught and silently ignored, hiding real failures.

**Before**

```python
try:
    risky()
except Exception:
    pass  # swallowed

```

**After**

```java
try:
    risky()
except SpecificError as exc:
    logger.warning("risky() failed: %s", exc)
    raise  # or convert to a domain error

```

---

## 3. Replace Magic Number with Named Constant

- **Location**: `sample-project/ecommerce/order_service.py:17 · OrderService.place_order`
- **Why**: unexplained literals: 100000, 5000, 86400

**Before**

```java
if len(items) > 86400: ...
```

**After**

```java
MAX_CACHE_SECONDS = 86_400

if len(items) > MAX_CACHE_SECONDS: ...

```

---

## 4. Replace Print with Structured Logging

- **Location**: `sample-project/ecommerce/order_service.py:17 · OrderService.place_order`
- **Why**: Debug prints leak into production output and lack severity/levels.

**Before**

```python
print("value:", x)  # or console.log / System.out.println
```

**After**

```java
logger.info("value", extra={"value": x})  # or log.info(f"value={x}")
```

---

## 5. Resolve Outstanding TODOs

- **Location**: `sample-project/ecommerce/order_service.py:17 · OrderService.place_order`
- **Why**: TODO/FIXME markers indicate unfinished work or known debt.

**Before**

```java
TODO: split this method, it does too much
```

**After**

```python
# Convert into a tracked issue, then implement or remove the marker.
```

---

## 6. Introduce Parameter Object

- **Location**: `sample-project/ecommerce/order_service.py:17 · OrderService.place_order`
- **Why**: 6 parameters (user_id, product_id, quantity, currency, coupon_code, rush) — group related data into a dataclass/record.

**Before**

```python
def place_order(user_id: int, product_id: int, quantity: int, currency: str, coupon_code: Optional[str], rush: bool) -> dict:
```

**After**

```python
            @dataclass
            class PlaceOrderConfig:
                user_id: int
product_id: int
quantity: int
currency: str
coupon_code: Optional[str]
rush: bool

            def place_order(config: PlaceOrderConfig) -> dict:
                ...

```

---

## 7. Decompose Conditional / Strategy Pattern

- **Location**: `sample-project/ecommerce/order_service.py:59 · OrderService.summarize_daily`
- **Why**: Cyclomatic complexity is 11 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 8. Replace Magic Number with Named Constant

- **Location**: `sample-project/ecommerce/order_service.py:59 · OrderService.summarize_daily`
- **Why**: unexplained literals: 100, 1000, 10000, 100000, 12000

**Before**

```java
if len(items) > 86400: ...
```

**After**

```java
MAX_CACHE_SECONDS = 86_400

if len(items) > MAX_CACHE_SECONDS: ...

```

---

## 9. Handle or Propagate the Exception

- **Location**: `sample-project/PaymentService.java:19 · PaymentService.authorizePayment`
- **Why**: An exception is caught and silently ignored, hiding real failures.

**Before**

```python
try:
    risky()
except Exception:
    pass  # swallowed

```

**After**

```java
try:
    risky()
except SpecificError as exc:
    logger.warning("risky() failed: %s", exc)
    raise  # or convert to a domain error

```

---

## 10. Replace Print with Structured Logging

- **Location**: `sample-project/PaymentService.java:44 · PaymentService.capture`
- **Why**: Debug prints leak into production output and lack severity/levels.

**Before**

```python
print("value:", x)  # or console.log / System.out.println
```

**After**

```java
logger.info("value", extra={"value": x})  # or log.info(f"value={x}")
```

---

## 11. Resolve Outstanding TODOs

- **Location**: `sample-project/PaymentService.java:44 · PaymentService.capture`
- **Why**: TODO/FIXME markers indicate unfinished work or known debt.

**Before**

```java
FIXME: idempotency not implemented
```

**After**

```python
# Convert into a tracked issue, then implement or remove the marker.
```

---

## 12. Replace Print with Structured Logging

- **Location**: `sample-project/userService.ts:14 · UserService.registerUser`
- **Why**: Debug prints leak into production output and lack severity/levels.

**Before**

```python
print("value:", x)  # or console.log / System.out.println
```

**After**

```java
logger.info("value", extra={"value": x})  # or log.info(f"value={x}")
```

---

