# API Reference

Auto-generated for `sample-project` — 19 functions across 6 files.

## Cpp

### `discount_engine.cpp`

####  🔧 `class DiscountEngine`

<a id="DiscountEngine-applyDiscount-5"></a>

##### `DiscountEngine.applyDiscount(price: double, tier: std::string, loyalty: bool, months: int)` → `double`

member of `DiscountEngine` · `sample-project/discount_engine.cpp:5` · LOC **24** · complexity **6** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `price` | `double` | `—` |
| `tier` | `std::string` | `—` |
| `loyalty` | `bool` | `—` |
| `months` | `int` | `—` |

**Returns** `double`

**Example**

```cpp
DiscountEngine obj;
auto result = obj.applyDiscount(price, tier, loyalty, months);
```

<a id="DiscountEngine-logApplied-29"></a>

##### `DiscountEngine.logApplied(entries: std::vector<std::string>, label: std::string)` → `void`

member of `DiscountEngine` · `sample-project/discount_engine.cpp:29` · LOC **5** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `entries` | `std::vector<std::string>` | `—` |
| `label` | `std::string` | `—` |

**Returns** `void`

**Example**

```cpp
DiscountEngine obj;
auto result = obj.logApplied(entries, label);
```

---

## Java

### `PaymentService.java`

####  🔧 `class PaymentService`

<a id="PaymentService-authorizePayment-19"></a>

##### `PaymentService.authorizePayment(userId: String, amount: double, currency: String, method: String, retry: boolean)` → `boolean`

member of `PaymentService` · `sample-project/PaymentService.java:19` · LOC **16** · complexity **6** · nesting **2**

**Description**

Authorizes a payment, converting currency if required.
/

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `userId` | `String` | `—` |
| `amount` | `double` | `—` |
| `currency` | `String` | `—` |
| `method` | `String` | `—` |
| `retry` | `boolean` | `—` |

**Returns** `boolean`

**Example**

```java
var obj = new PaymentService();
var result = obj.authorizePayment(userId, amount, currency, method, retry);
```

<a id="PaymentService-doAuthorize-37"></a>

##### `PaymentService.doAuthorize(userId: String, amount: double, method: String)` → `boolean`

member of `PaymentService` · `sample-project/PaymentService.java:37` · LOC **2** · complexity **3** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `userId` | `String` | `—` |
| `amount` | `double` | `—` |
| `method` | `String` | `—` |

**Returns** `boolean`

**Example**

```java
var obj = new PaymentService();
var result = obj.doAuthorize(userId, amount, method);
```

<a id="PaymentService-capture-44"></a>

##### `PaymentService.capture(paymentId: String, metadata: List<String>)` → `void`

member of `PaymentService` · `sample-project/PaymentService.java:44` · LOC **3** · complexity **1** · nesting **0**

**Description**

Captures a previously authorized payment.
/

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `paymentId` | `String` | `—` |
| `metadata` | `List<String>` | `—` |

**Returns** `void`

**Example**

```java
var obj = new PaymentService();
var result = obj.capture(paymentId, metadata);
```

---

## Python

### `ecommerce/inventory.py`

####  🔧 `class InventoryManager`

<a id="InventoryManager-__init__-9"></a>

##### `InventoryManager.__init__()`

member of `InventoryManager` · `sample-project/ecommerce/inventory.py:9` · LOC **5** · complexity **1** · nesting **0**

**Example**

```py
obj = InventoryManager()
result = obj.__init__()
```

<a id="InventoryManager-add_product-14"></a>

##### `InventoryManager.add_product(product_id: int, stock: int, price: float)` → `None`

member of `InventoryManager` · `sample-project/ecommerce/inventory.py:14` · LOC **5** · complexity **1** · nesting **0**

**Description**

Register a product with initial stock and price.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `product_id` | `int` | `—` |
| `stock` | `int` | `—` |
| `price` | `float` | `—` |

**Returns** `None`

**Example**

```py
obj = InventoryManager()
result = obj.add_product(product_id, stock, price)
```

<a id="InventoryManager-check_stock-19"></a>

##### `InventoryManager.check_stock(product_id: int)` → `int`

member of `InventoryManager` · `sample-project/ecommerce/inventory.py:19` · LOC **4** · complexity **1** · nesting **0**

**Description**

Return available units for a product.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `product_id` | `int` | `—` |

**Returns** `int`

**Example**

```py
obj = InventoryManager()
result = obj.check_stock(product_id)
```

<a id="InventoryManager-price_of-23"></a>

##### `InventoryManager.price_of(product_id: int)` → `float`

member of `InventoryManager` · `sample-project/ecommerce/inventory.py:23` · LOC **4** · complexity **1** · nesting **0**

**Description**

Return the unit price of a product.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `product_id` | `int` | `—` |

**Returns** `float`

**Example**

```py
obj = InventoryManager()
result = obj.price_of(product_id)
```

<a id="InventoryManager-reserve-27"></a>

##### `InventoryManager.reserve(product_id: int, quantity: int)` → `bool`

member of `InventoryManager` · `sample-project/ecommerce/inventory.py:27` · LOC **7** · complexity **2** · nesting **3**

**Description**

Reserve units if enough stock exists.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `product_id` | `int` | `—` |
| `quantity` | `int` | `—` |

**Returns** `bool`

**Example**

```py
obj = InventoryManager()
result = obj.reserve(product_id, quantity)
```

<a id="InventoryManager-release-34"></a>

##### `InventoryManager.release(order_id: int)` → `bool`

member of `InventoryManager` · `sample-project/ecommerce/inventory.py:34` · LOC **4** · complexity **1** · nesting **0**

**Description**

Release a reservation (stub for demo).

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `order_id` | `int` | `—` |

**Returns** `bool`

**Example**

```py
obj = InventoryManager()
result = obj.release(order_id)
```

---

### `ecommerce/order_service.py`

####  🔧 `class OrderService`

<a id="OrderService-__init__-12"></a>

##### `OrderService.__init__(inventory: InventoryManager, discount_rate: float = 0.0)`

member of `OrderService` · `sample-project/ecommerce/order_service.py:12` · LOC **5** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `inventory` | `InventoryManager` | `—` |
| `discount_rate` | `float` | `0.0` |

**Example**

```py
obj = OrderService()
result = obj.__init__(inventory, discount_rate)
```

<a id="OrderService-place_order-17"></a>

##### `OrderService.place_order(user_id: int, product_id: int, quantity: int, currency: str = "USD", coupon_code: Optional[str] = None, rush: bool = False)` → `dict`

member of `OrderService` · `sample-project/ecommerce/order_service.py:17` · LOC **35** · complexity **8** · nesting **7**

**Description**

Place an order for a product.

        Validates stock, applies discounts, computes totals and persists the order.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `user_id` | `int` | `—` |
| `product_id` | `int` | `—` |
| `quantity` | `int` | `—` |
| `currency` | `str` | `"USD"` |
| `coupon_code` | `Optional[str]` | `None` |
| `rush` | `bool` | `False` |

**Returns** `dict`

**Example**

```py
obj = OrderService()
result = obj.place_order(user_id, product_id, quantity, currency, coupon_code, rush)
```

<a id="OrderService-cancel_order-52"></a>

##### `OrderService.cancel_order(order_id: int, reason: str = "user request")` → `bool`

member of `OrderService` · `sample-project/ecommerce/order_service.py:52` · LOC **7** · complexity **1** · nesting **0**

**Description**

Cancel an existing order and release reserved stock.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `order_id` | `int` | `—` |
| `reason` | `str` | `"user request"` |

**Returns** `bool`

**Example**

```py
obj = OrderService()
result = obj.cancel_order(order_id, reason)
```

<a id="OrderService-summarize_daily-59"></a>

##### `OrderService.summarize_daily(orders: list, threshold: float = 100.0)` → `dict`

member of `OrderService` · `sample-project/ecommerce/order_service.py:59` · LOC **26** · complexity **11** · nesting **3**

**Description**

Summarize a day's orders into aggregate metrics.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `orders` | `list` | `—` |
| `threshold` | `float` | `100.0` |

**Returns** `dict`

**Example**

```py
obj = OrderService()
result = obj.summarize_daily(orders, threshold)
```

---

## Typescript

### `userService.ts`

####  📐 `interface User`

> User management with registration and profile lookups.

####  🔧 `class UserService`

<a id="normalizeEmail-38"></a>

##### `normalizeEmail(raw: string)` → `string`

`sample-project/userService.ts:38` · LOC **2** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `raw` | `string` | `—` |

**Returns** `string`

**Example**

```ts
const result = normalizeEmail(raw);
```

<a id="UserService-registerUser-14"></a>

##### `UserService.registerUser(email: string, displayName: string, password: string, newsletter: boolean, tier: string)` → `User`

member of `UserService` · `sample-project/userService.ts:14` · LOC **6** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `email` | `string` | `—` |
| `displayName` | `string` | `—` |
| `password` | `string` | `—` |
| `newsletter` | `boolean` | `—` |
| `tier` | `string` | `—` |

**Returns** `User`

**Example**

```ts
const obj = new UserService();
const result = obj.registerUser(email, displayName, password, newsletter, tier);
```

<a id="UserService-findUser-22"></a>

##### `UserService.findUser(id: number)` → `User | undefined`

member of `UserService` · `sample-project/userService.ts:22` · LOC **2** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `id` | `number` | `—` |

**Returns** `User | undefined`

**Example**

```ts
const obj = new UserService();
const result = obj.findUser(id);
```

<a id="UserService-fetchProfile-26"></a>

##### `UserService.fetchProfile(url: string, timeoutMs: number)` → `Promise<string>`

member of `UserService` · `sample-project/userService.ts:26` · LOC **9** · complexity **1** · nesting **1**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `url` | `string` | `—` |
| `timeoutMs` | `number` | `—` |

**Returns** `Promise<string>`

**Example**

```ts
const obj = new UserService();
const result = obj.fetchProfile(url, timeoutMs);
```

---
