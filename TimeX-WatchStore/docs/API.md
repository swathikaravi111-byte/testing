# TimeX API Documentation

Complete API reference for TimeX Watch Store.

## Base URL

```
Production: https://api.timex.com/api
Development: http://localhost:5000/api
```

## Authentication

All endpoints except public ones require JWT token in Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Response Format

All responses are in JSON format with status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Server Error

## Endpoints

### Auth Endpoints

#### Register
- **POST** `/auth/register`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "Password@123",
    "firstName": "John",
    "lastName": "Doe"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "isSuccess": true,
    "message": "Registration successful",
    "user": {
      "id": "uuid",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "Customer"
    },
    "token": "jwt_token",
    "refreshToken": "refresh_token"
  }
  ```

#### Login
- **POST** `/auth/login`
- **Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "Password@123"
  }
  ```
- **Response:** `200 OK` (same as register)

#### Refresh Token
- **POST** `/auth/refresh`
- **Auth:** Not required
- **Body:**
  ```json
  {
    "refreshToken": "refresh_token"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "isSuccess": true,
    "message": "Token refreshed",
    "token": "new_jwt_token",
    "refreshToken": "new_refresh_token"
  }
  ```

#### Logout
- **POST** `/auth/logout`
- **Auth:** Required
- **Response:** `200 OK`

### Product Endpoints

#### Get All Products
- **GET** `/products`
- **Auth:** Not required
- **Response:** `200 OK` - Array of products

#### Get Product by ID
- **GET** `/products/{id}`
- **Auth:** Not required
- **Response:** `200 OK`

#### Search Products
- **GET** `/products/search/{query}`
- **Auth:** Not required
- **Response:** `200 OK` - Matching products

#### Filter Products
- **POST** `/products/filter`
- **Auth:** Not required
- **Body:**
  ```json
  {
    "brand": "Rolex",
    "minPrice": 1000,
    "maxPrice": 10000,
    "categoryId": "uuid",
    "material": "Gold"
  }
  ```
- **Response:** `200 OK` - Filtered products

#### Create Product (Admin)
- **POST** `/products`
- **Auth:** Required (Admin)
- **Body:** Product creation data
- **Response:** `201 Created`

#### Update Product (Admin)
- **PUT** `/products/{id}`
- **Auth:** Required (Admin)
- **Response:** `200 OK`

#### Delete Product (Admin)
- **DELETE** `/products/{id}`
- **Auth:** Required (Admin)
- **Response:** `200 OK`

### Cart Endpoints

#### Get Cart
- **GET** `/cart`
- **Auth:** Required
- **Response:** `200 OK`
  ```json
  {
    "userId": "uuid",
    "items": [
      {
        "id": "uuid",
        "productId": "uuid",
        "productName": "Watch Name",
        "quantity": 1,
        "unitPrice": 1000,
        "totalPrice": 1000
      }
    ],
    "totalPrice": 1000
  }
  ```

#### Add to Cart
- **POST** `/cart/add`
- **Auth:** Required
- **Body:**
  ```json
  {
    "productId": "uuid",
    "quantity": 1
  }
  ```
- **Response:** `200 OK` - Added item

#### Update Cart Item
- **PUT** `/cart/{itemId}`
- **Auth:** Required
- **Body:**
  ```json
  {
    "quantity": 2
  }
  ```
- **Response:** `200 OK`

#### Remove from Cart
- **DELETE** `/cart/{itemId}`
- **Auth:** Required
- **Response:** `200 OK`

#### Clear Cart
- **DELETE** `/cart`
- **Auth:** Required
- **Response:** `200 OK`

### Order Endpoints

#### Get User Orders
- **GET** `/orders`
- **Auth:** Required
- **Response:** `200 OK` - Array of orders

#### Get Order by ID
- **GET** `/orders/{id}`
- **Auth:** Required
- **Response:** `200 OK`

#### Create Order
- **POST** `/orders`
- **Auth:** Required
- **Body:**
  ```json
  {
    "shippingAddress": "123 Main St",
    "billingAddress": "123 Main St",
    "shippingMethod": "standard"
  }
  ```
- **Response:** `201 Created`

#### Get All Orders (Admin)
- **GET** `/orders/admin/all`
- **Auth:** Required (Admin)
- **Response:** `200 OK`

#### Update Order Status (Admin)
- **PUT** `/orders/{id}/status`
- **Auth:** Required (Admin)
- **Body:**
  ```json
  {
    "status": "Shipped"
  }
  ```
- **Response:** `200 OK`

### User Endpoints

#### Get Profile
- **GET** `/users/profile`
- **Auth:** Required
- **Response:** `200 OK`

#### Update Profile
- **PUT** `/users/profile`
- **Auth:** Required
- **Body:** Updated profile data
- **Response:** `200 OK`

### Wishlist Endpoints

#### Get Wishlist
- **GET** `/wishlist`
- **Auth:** Required
- **Response:** `200 OK`

#### Add to Wishlist
- **POST** `/wishlist/{productId}`
- **Auth:** Required
- **Response:** `200 OK`

#### Remove from Wishlist
- **DELETE** `/wishlist/{productId}`
- **Auth:** Required
- **Response:** `200 OK`

### Review Endpoints

#### Get Product Reviews
- **GET** `/reviews/product/{productId}`
- **Auth:** Not required
- **Response:** `200 OK` - Array of reviews

#### Create Review
- **POST** `/reviews`
- **Auth:** Required
- **Body:**
  ```json
  {
    "productId": "uuid",
    "rating": 5,
    "title": "Great watch!",
    "comment": "Excellent quality and fast shipping"
  }
  ```
- **Response:** `201 Created`

#### Update Review
- **PUT** `/reviews/{id}`
- **Auth:** Required
- **Response:** `200 OK`

#### Delete Review
- **DELETE** `/reviews/{id}`
- **Auth:** Required
- **Response:** `200 OK`

### Chatbot Endpoints

#### Send Message
- **POST** `/chatbot/message`
- **Auth:** Required
- **Body:**
  ```json
  {
    "message": "What luxury watches do you have?"
  }
  ```
- **Response:** `200 OK`
  ```json
  {
    "response": "We have Rolex, Omega, and Cartier luxury watches..."
  }
  ```

### Admin Endpoints

#### Get Dashboard
- **GET** `/admin/dashboard`
- **Auth:** Required (Admin)
- **Response:** `200 OK`
  ```json
  {
    "totalUsers": 100,
    "totalProducts": 50,
    "totalOrders": 200,
    "totalRevenue": 500000
  }
  ```

#### Get Sales Reports
- **GET** `/admin/reports`
- **Auth:** Required (Admin)
- **Response:** `200 OK` - Array of daily reports

## Error Responses

```json
{
  "message": "Error description",
  "errors": [
    {
      "field": "email",
      "message": "Email is required"
    }
  ]
}
```

## Rate Limiting

- Standard: 100 requests/minute
- Premium: 1000 requests/minute
- Burst: 10 requests/second

## Pagination

Use `?page=1&limit=10` query parameters for paginated responses.

## Filtering

Use query parameters for filtering:
- `?minPrice=1000&maxPrice=5000`
- `?brand=Rolex&category=Luxury`
- `?searchTerm=submariner`

---

**Last Updated:** 2024
**API Version:** 1.0.0
