# Code Quality Report

_Generated 2026-09-23T11:32:18+00:00_

## Smell Summary

| Smell | Occurrences | Severity |
|---|---|---|
| Print Debugging | 3 | low |
| Empty Catch Block | 2 | high |
| TODO/FIXME Left In Code | 2 | low |
| Magic Numbers | 2 | low |
| Deep Nesting | 1 | medium |
| Too Many Parameters | 1 | medium |
| High Cyclomatic Complexity | 1 | high |

**Total findings**: 12

## Findings Detail

- **[HIGH] Empty Catch Block** — `PaymentService.authorizePayment` (`PaymentService.java:19`) — exception handler body is empty
- **[LOW] Print Debugging** — `PaymentService.capture` (`PaymentService.java:44`) — debug print statement left in production code
- **[LOW] TODO/FIXME Left In Code** — `PaymentService.capture` (`PaymentService.java:44`) — FIXME: idempotency not implemented
- **[MEDIUM] Deep Nesting** — `OrderService.place_order` (`ecommerce/order_service.py:17`) — nesting depth = 7
- **[MEDIUM] Too Many Parameters** — `OrderService.place_order` (`ecommerce/order_service.py:17`) — 6 parameters
- **[HIGH] Empty Catch Block** — `OrderService.place_order` (`ecommerce/order_service.py:17`) — exception handler body is empty
- **[LOW] Magic Numbers** — `OrderService.place_order` (`ecommerce/order_service.py:17`) — unexplained literals: 100000, 5000, 86400
- **[LOW] Print Debugging** — `OrderService.place_order` (`ecommerce/order_service.py:17`) — debug print statement left in production code
- **[LOW] TODO/FIXME Left In Code** — `OrderService.place_order` (`ecommerce/order_service.py:17`) — TODO: split this method, it does too much
- **[HIGH] High Cyclomatic Complexity** — `OrderService.summarize_daily` (`ecommerce/order_service.py:59`) — cyclomatic complexity = 11
- **[LOW] Magic Numbers** — `OrderService.summarize_daily` (`ecommerce/order_service.py:59`) — unexplained literals: 100, 1000, 10000, 100000, 12000
- **[LOW] Print Debugging** — `UserService.registerUser` (`userService.ts:14`) — debug print statement left in production code

## Complexity Hotspots

| Function | File | CX | LOC | Nesting |
|---|---|---|---|---|
| `OrderService.summarize_daily` | `ecommerce/order_service.py` | 11 | 26 | 3 |
| `OrderService.place_order` | `ecommerce/order_service.py` | 8 | 35 | 7 |
| `DiscountEngine.applyDiscount` | `discount_engine.cpp` | 6 | 24 | 3 |
| `PaymentService.authorizePayment` | `PaymentService.java` | 6 | 16 | 2 |
| `PaymentService.doAuthorize` | `PaymentService.java` | 3 | 2 | 0 |
| `InventoryManager.reserve` | `ecommerce/inventory.py` | 2 | 7 | 3 |
| `PaymentService.capture` | `PaymentService.java` | 1 | 3 | 0 |
| `DiscountEngine.logApplied` | `discount_engine.cpp` | 1 | 5 | 0 |
| `normalizeEmail` | `userService.ts` | 1 | 2 | 0 |
| `UserService.registerUser` | `userService.ts` | 1 | 6 | 0 |
