# Database Design Document

## Overview

TimeX uses PostgreSQL 15 with Entity Framework Core for data persistence and management.

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone_number VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    role INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    refresh_token VARCHAR(255),
    refresh_token_expiry_time TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Categories Table
```sql
CREATE TABLE categories (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    image_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Products Table
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sku VARCHAR(50) UNIQUE NOT NULL,
    price DECIMAL(18,2) NOT NULL,
    discount_price DECIMAL(18,2),
    brand VARCHAR(100) NOT NULL,
    category_id UUID REFERENCES categories(id),
    model VARCHAR(100),
    water_resistance VARCHAR(50),
    material VARCHAR(100),
    movement VARCHAR(50),
    diameter VARCHAR(50),
    color VARCHAR(50),
    average_rating DECIMAL(3,2) DEFAULT 0,
    total_reviews INT DEFAULT 0,
    image_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_products_sku ON products(sku);
```

### CartItems Table
```sql
CREATE TABLE cart_items (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    product_id UUID NOT NULL REFERENCES products(id),
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(18,2) NOT NULL,
    added_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_cart_items_user ON cart_items(user_id);
```

### Orders Table
```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES users(id),
    status INT DEFAULT 0,
    total_amount DECIMAL(18,2) NOT NULL,
    tax_amount DECIMAL(18,2),
    shipping_cost DECIMAL(18,2),
    shipping_address VARCHAR(255),
    billing_address VARCHAR(255),
    shipping_method VARCHAR(50),
    tracking_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_number ON orders(order_number);
```

### OrderItems Table
```sql
CREATE TABLE order_items (
    id UUID PRIMARY KEY,
    order_id UUID NOT NULL REFERENCES orders(id),
    product_id UUID NOT NULL REFERENCES products(id),
    quantity INT NOT NULL,
    unit_price DECIMAL(18,2) NOT NULL,
    total_price DECIMAL(18,2) NOT NULL
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
```

### Reviews Table
```sql
CREATE TABLE reviews (
    id UUID PRIMARY KEY,
    product_id UUID NOT NULL REFERENCES products(id),
    user_id UUID NOT NULL REFERENCES users(id),
    rating INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    comment VARCHAR(2000),
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    helpful_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reviews_product ON reviews(product_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);
```

### WishlistItems Table
```sql
CREATE TABLE wishlist_items (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    product_id UUID NOT NULL REFERENCES products(id),
    added_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_wishlist_user ON wishlist_items(user_id);
```

### Inventory Table
```sql
CREATE TABLE inventory (
    id UUID PRIMARY KEY,
    product_id UUID NOT NULL UNIQUE REFERENCES products(id),
    quantity INT NOT NULL,
    reserved_quantity INT DEFAULT 0,
    minimum_stock_level INT DEFAULT 5,
    warehouse_location VARCHAR(100),
    last_restocked_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_inventory_product ON inventory(product_id);
```

### ChatMessages Table
```sql
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    message_type INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_chat_messages_user ON chat_messages(user_id);
```

## Entity Relationships

```
Users (1) ---> (*) Orders
Users (1) ---> (*) CartItems
Users (1) ---> (*) Reviews
Users (1) ---> (*) WishlistItems
Users (1) ---> (*) ChatMessages

Products (1) ---> (*) CartItems
Products (1) ---> (*) OrderItems
Products (1) ---> (*) Reviews
Products (1) ---> (*) WishlistItems
Products (1) ---> (1) Inventory

Categories (1) ---> (*) Products

Orders (1) ---> (*) OrderItems
OrderItems (*) ---> (1) Products
```

## Data Types

| Type | Usage |
|------|-------|
| UUID | Primary keys, foreign keys |
| VARCHAR | Text fields with max length |
| TEXT | Long text fields |
| INT | Integers |
| DECIMAL(18,2) | Currency values |
| TIMESTAMP | Date/time tracking |
| BOOLEAN | Boolean flags |

## Indexing Strategy

### Primary Indexes
- All primary keys: `id`
- Foreign keys for joins
- Unique columns: `email`, `sku`, `order_number`

### Secondary Indexes
- Frequently filtered: `category_id`, `brand`, `user_id`
- Search columns: `name`, `sku`
- Status tracking: `status`, `is_active`

### Query Performance
```sql
-- Analyze query performance
EXPLAIN ANALYZE
SELECT * FROM products
WHERE brand = 'Rolex' AND price < 10000;

-- Check index usage
SELECT * FROM pg_stat_user_indexes;
```

## Constraints

### Unique Constraints
- `email` on Users table
- `sku` on Products table
- `order_number` on Orders table

### Foreign Key Constraints
- Cascading delete for related records
- Restrict delete if referenced

### Check Constraints
- Rating: 1-5
- Stock level: >= 0
- Price: > 0

## Backup Strategy

### Daily Backups
```bash
pg_dump -U postgres TimeXDB > backup_$(date +%Y%m%d).sql
```

### Point-in-Time Recovery
```bash
# Enable WAL archiving in postgresql.conf
archive_mode = on
archive_command = 'cp %p /backup/wal_archive/%f'
```

## Maintenance

### Vacuum
```sql
VACUUM ANALYZE;
```

### Monitor Database Size
```sql
SELECT datname, pg_size_pretty(pg_database_size(datname))
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
```

---

**Last Updated:** 2024
**Version:** 1.0.0
