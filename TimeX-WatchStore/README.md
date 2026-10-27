# TimeX AI Watch Store

A production-ready e-commerce platform for selling luxury and premium watches, featuring AI-powered recommendations and customer support.

## 🎯 Overview

TimeX AI Watch Store is a full-stack web application built with:
- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: ASP.NET Core 8.0 Web API
- **Database**: PostgreSQL
- **AI**: Integration with OpenAI for watch recommendations and customer support

## ✨ Key Features

### Customer Features
- 🔐 User registration and authentication (JWT)
- 👁️ Browse watches by category, brand, and price
- 🔍 Advanced search and filtering
- ❤️ Wishlist management
- 🛒 Shopping cart with real-time updates
- 💳 Secure checkout process
- 📦 Order history and tracking
- ⭐ Product reviews and ratings
- 👤 User profile management

### AI Chatbot Features
- 💡 Intelligent watch recommendations based on budget
- 🔄 Watch model comparisons
- 🎯 Occasion-based suggestions
- 📊 Specification explanations
- 📦 Order status tracking
- ❓ FAQ responses
- 🆘 24/7 Customer support

### Admin Features
- 📊 Dashboard with analytics
- 📦 Product management
- 📈 Inventory management
- 👥 User management
- 📋 Order management
- 📈 Sales reports

## 🏗️ Project Structure

```
TimeX-WatchStore/
├── backend/                 # ASP.NET Core API
│   ├── TimeX.API/
│   ├── TimeX.Data/
│   ├── TimeX.Business/
│   ├── TimeX.Tests/
│   └── docker/
├── frontend/                # React TypeScript
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── utils/
│   ├── public/
│   └── docker/
├── docs/                    # Documentation
├── .github/workflows/       # CI/CD
└── docker-compose.yml       # Docker orchestration
```

## 🚀 Quick Start

### Prerequisites
- .NET 8.0 SDK
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Backend Setup
```bash
cd backend
dotnet restore
dotnet ef database update
dotnet run
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Setup
```bash
docker-compose up -d
```

## 📚 Documentation

- [Architecture Guide](docs/Architecture.md) - System design and components
- [Database Design](docs/DatabaseDesign.md) - Schema and relationships
- [API Documentation](docs/API.md) - Endpoints and integration
- [Deployment Guide](docs/DeploymentGuide.md) - Production deployment
- [User Guide](docs/UserGuide.md) - End-user documentation
- [Admin Guide](docs/AdminGuide.md) - Administrator documentation
- [AI Chatbot Design](docs/AIChatbotDesign.md) - Chatbot architecture
- [Work Log](docs/WorkLog.md) - Development progress
- [Change Log](docs/ChangeLog.md) - Feature history

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - User logout

### Products
- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get product details
- `GET /api/products/category/{category}` - Filter by category
- `POST /api/products` - Create product (Admin)
- `PUT /api/products/{id}` - Update product (Admin)
- `DELETE /api/products/{id}` - Delete product (Admin)

### Cart
- `GET /api/cart` - Get cart items
- `POST /api/cart` - Add to cart
- `PUT /api/cart/{itemId}` - Update cart item
- `DELETE /api/cart/{itemId}` - Remove from cart

### Orders
- `GET /api/orders` - Get user orders
- `GET /api/orders/{id}` - Get order details
- `POST /api/orders` - Create order
- `PUT /api/orders/{id}/status` - Update order status (Admin)

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile
- `DELETE /api/users/{id}` - Delete user (Admin)

### Wishlist
- `GET /api/wishlist` - Get wishlist
- `POST /api/wishlist` - Add to wishlist
- `DELETE /api/wishlist/{productId}` - Remove from wishlist

### Reviews
- `GET /api/reviews/{productId}` - Get product reviews
- `POST /api/reviews` - Create review
- `PUT /api/reviews/{id}` - Update review
- `DELETE /api/reviews/{id}` - Delete review

### Admin
- `GET /api/admin/dashboard` - Dashboard analytics
- `GET /api/admin/orders` - All orders
- `GET /api/admin/users` - All users
- `GET /api/admin/reports` - Sales reports

## 🤖 AI Chatbot Endpoints

- `POST /api/chat/message` - Send message to chatbot
- `POST /api/chat/recommend` - Get watch recommendations
- `POST /api/chat/compare` - Compare watches
- `GET /api/chat/faq` - Get FAQ responses

## 🔐 Security

- JWT token-based authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- CORS configuration
- Rate limiting
- SQL injection prevention
- XSS protection
- CSRF protection

## 🧪 Testing

```bash
# Backend tests
cd backend
dotnet test

# Frontend tests
cd frontend
npm test

# Coverage
npm run test:coverage
```

## 📦 Deployment

### Production Build
```bash
# Backend
cd backend
dotnet publish -c Release

# Frontend
cd frontend
npm run build
```

### Environment Configuration
Create `.env` files for each environment:
- `.env.development` - Development
- `.env.staging` - Staging
- `.env.production` - Production

## 🐳 Docker Deployment

```bash
docker-compose -f docker-compose.yml up -d
```

See [DeploymentGuide.md](docs/DeploymentGuide.md) for detailed instructions.

## 📊 Database Schema

Key entities:
- **Users** - Customer and admin accounts
- **Products** - Watch inventory
- **Categories** - Product categories
- **Brands** - Watch brands
- **Cart** - Shopping cart items
- **Orders** - Customer orders
- **OrderItems** - Order line items
- **Reviews** - Product reviews
- **Wishlist** - Saved items
- **Inventory** - Stock management

## 🎯 Technology Stack

### Backend
- ASP.NET Core 8.0
- Entity Framework Core 8.0
- PostgreSQL
- JWT Authentication
- Swagger/OpenAPI

### Frontend
- React 18
- TypeScript 5
- Tailwind CSS
- Redux Toolkit
- Axios
- React Router v6

### AI/ML
- OpenAI GPT-4 Integration
- Prompt Engineering
- Context Management

### DevOps
- Docker & Docker Compose
- GitHub Actions
- PostgreSQL
- Environment-based configuration

## 📝 License

Proprietary - All Rights Reserved

## 👥 Contributing

This is a production system. All changes should follow:
- Code review process
- Test coverage requirements
- Documentation updates
- Deployment procedures

## 📞 Support

For support, please contact:
- Development Team: dev@timex.local
- Admin Support: admin@timex.local
- Customer Support: support@timex.local

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production Ready
