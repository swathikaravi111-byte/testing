# TimeX AI Watch Store - Architecture Guide

## System Overview

TimeX is a modern, scalable e-commerce platform built with a microservices-ready architecture, featuring:
- **Frontend**: React with TypeScript and Tailwind CSS
- **Backend**: ASP.NET Core 8.0 Web API
- **Database**: PostgreSQL 15
- **AI Integration**: OpenAI GPT-4 for chatbot
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  React SPA (TypeScript + Tailwind CSS)                 │  │
│  │  - Product Browsing                                    │  │
│  │  - Shopping Cart                                       │  │
│  │  - Checkout                                            │  │
│  │  - User Profile                                        │  │
│  │  - Admin Dashboard                                     │  │
│  │  - Chat Integration                                    │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│                  API Gateway Layer (Nginx)                   │
│  - Request Routing                                           │
│  - SSL/TLS Termination                                       │
│  - Load Balancing                                            │
│  - CORS Handling                                             │
└─────────────────────────────────────────────────────────────┘
                          ↓ REST API
┌─────────────────────────────────────────────────────────────┐
│                 Application Layer (ASP.NET Core)             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Controllers                                             │ │
│  │  - AuthController                                        │ │
│  │  - ProductsController                                    │ │
│  │  - CartController                                        │ │
│  │  - OrdersController                                      │ │
│  │  - UsersController                                       │ │
│  │  - ReviewsController                                     │ │
│  │  - ChatbotController                                     │ │
│  │  - AdminController                                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Business Logic Layer (Services)                         │ │
│  │  - AuthService (JWT, Registration, Login)                │ │
│  │  - ProductService (CRUD, Search, Filter)                 │ │
│  │  - CartService (Add, Remove, Update)                     │ │
│  │  - OrderService (Create, Status, Tracking)               │ │
│  │  - UserService (Profile Management)                      │ │
│  │  - WishlistService                                        │ │
│  │  - ReviewService                                          │ │
│  │  - ChatbotService (AI Integration)                        │ │
│  │  - InventoryService                                       │ │
│  │  - AdminService (Analytics, Reports)                      │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Data Access Layer (Entity Framework Core)               │ │
│  │  - Repository Pattern                                    │ │
│  │  - LINQ Queries                                          │ │
│  │  - Migrations                                            │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          ↓ SQL
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer (PostgreSQL)                   │
│  - Users & Authentication                                    │
│  - Products & Inventory                                      │
│  - Orders & Order Items                                      │
│  - Reviews & Ratings                                         │
│  - Wishlist Items                                            │
│  - Chat Messages                                             │
│  - Categories & Brands                                       │
└─────────────────────────────────────────────────────────────┘
                          ↓ API
┌─────────────────────────────────────────────────────────────┐
│                 External Services                            │
│  - OpenAI API (Chatbot, Recommendations)                    │
│  - Payment Gateway (Future)                                 │
│  - Email Service (Future)                                   │
│  - SMS Service (Future)                                     │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (React + TypeScript)

**Structure:**
```
frontend/src/
├── components/        # Reusable UI components
│   ├── Navbar.tsx
│   ├── Footer.tsx
│   └── ProtectedRoute.tsx
├── pages/            # Page components
│   ├── HomePage.tsx
│   ├── ProductPage.tsx
│   ├── CartPage.tsx
│   ├── CheckoutPage.tsx
│   ├── OrdersPage.tsx
│   ├── ProfilePage.tsx
│   ├── AdminDashboard.tsx
│   ├── LoginPage.tsx
│   └── RegisterPage.tsx
├── services/         # API communication
│   └── api.ts       # Axios instance with interceptors
├── store/           # Zustand store (state management)
│   ├── authStore.ts
│   └── cartStore.ts
├── types/           # TypeScript interfaces
│   └── index.ts
├── App.tsx          # Main app with routing
└── main.tsx         # Entry point
```

**Key Features:**
- Responsive design with Tailwind CSS
- Protected routes for authenticated users
- Role-based access control (Admin)
- Real-time cart updates with Zustand
- Axios interceptors for JWT auth
- Error handling and user feedback

### Backend (ASP.NET Core)

**Project Structure:**
```
backend/
├── TimeX.API/           # Web API project
│   ├── Controllers/     # API endpoints
│   ├── Program.cs       # Startup configuration
│   └── appsettings.json # Configuration
├── TimeX.Data/          # Data layer
│   ├── Entities/        # Domain models
│   ├── TimeXDbContext.cs
│   └── DatabaseSeeder.cs
├── TimeX.Business/      # Business logic
│   └── Services/        # Service implementations
└── TimeX.Tests/         # Unit tests
```

**Architecture Layers:**

1. **Controllers Layer**
   - HTTP request handling
   - Input validation
   - Response formatting
   - Authorization checks

2. **Service Layer**
   - Business logic implementation
   - Data validation
   - Cross-cutting concerns
   - Service orchestration

3. **Data Access Layer**
   - EF Core DbContext
   - LINQ queries
   - Database migrations
   - Connection pooling

### Database Schema

**Core Entities:**

- **Users**: Customer and admin accounts
- **Products**: Watch inventory
- **Categories**: Product categories
- **Cart**: Shopping cart items
- **Orders**: Customer orders
- **OrderItems**: Line items in orders
- **Reviews**: Product reviews
- **Wishlist**: Saved items
- **Inventory**: Stock management
- **ChatMessages**: Chat history

**Relationships:**
- User → Orders (One-to-Many)
- User → CartItems (One-to-Many)
- User → Reviews (One-to-Many)
- Product → CartItems (One-to-Many)
- Product → OrderItems (One-to-Many)
- Product → Reviews (One-to-Many)
- Order → OrderItems (One-to-Many)

## Security Architecture

### Authentication
- JWT (JSON Web Tokens) for stateless authentication
- Bearer token in Authorization header
- Refresh token rotation for extended sessions
- bcrypt for password hashing

### Authorization
- Role-based access control (RBAC)
- Admin role for protected endpoints
- User verification for personal data access

### Data Protection
- HTTPS/TLS for transport security
- CORS configuration for allowed origins
- Input validation and sanitization
- SQL injection prevention via parameterized queries
- XSS protection with content type headers

### API Security
- Rate limiting (future enhancement)
- API key authentication (future)
- Request signing (future)
- Audit logging (future)

## Deployment Architecture

### Development
- Local PostgreSQL instance
- ASP.NET Core development server
- React development server with hot reload
- Direct API calls without proxy

### Docker Compose
- PostgreSQL container
- ASP.NET Core API container
- React frontend container (Nginx)
- Nginx reverse proxy

### Production
- Kubernetes or Docker Swarm (recommended)
- PostgreSQL managed service
- Load balancer (ALB/NLB)
- CDN for static assets
- Database replication and backups

## Scalability Considerations

1. **Horizontal Scaling**
   - Stateless API design
   - Load balancer distribution
   - Database connection pooling

2. **Caching Strategy**
   - Redis for session cache (future)
   - CDN for static assets
   - Browser caching headers

3. **Database Optimization**
   - Indexes on frequently queried columns
   - Query optimization and monitoring
   - Read replicas for read-heavy operations

4. **API Rate Limiting**
   - Per-user rate limits
   - Endpoint-specific throttling
   - Graceful degradation

## Performance Optimization

1. **Frontend**
   - Code splitting with React Router
   - Lazy loading of components
   - Image optimization
   - Bundle size monitoring

2. **Backend**
   - Query optimization and N+1 prevention
   - Response caching
   - Database indexing
   - Async/await for I/O operations

3. **Network**
   - Compression (Gzip)
   - HTTP/2 support
   - Content delivery network
   - Minimize payload size

## Monitoring and Logging

- Application logs with structured logging
- Error tracking and reporting
- Performance monitoring
- User analytics
- Security audit logs

## Integration Points

1. **OpenAI API** - Chatbot and recommendations
2. **Payment Gateway** - Transaction processing
3. **Email Service** - Notifications
4. **SMS Service** - Order updates
5. **Analytics Platform** - User behavior tracking

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript 5, Tailwind CSS |
| Backend | ASP.NET Core 8, C# |
| Database | PostgreSQL 15 |
| ORM | Entity Framework Core 8 |
| Cache | Zustand (Client), Redis (Server - Future) |
| Authentication | JWT, bcrypt |
| Testing | xUnit, Moq, Vitest |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| API Documentation | Swagger/OpenAPI |

---

**Last Updated:** 2024
**Version:** 1.0.0
**Status:** Production Ready
