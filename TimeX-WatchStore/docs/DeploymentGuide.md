# Deployment Guide

## Development Setup

### Prerequisites
- .NET 8.0 SDK
- Node.js 18+
- PostgreSQL 15
- Docker & Docker Compose (optional)

### Local Setup

#### Backend
```bash
cd backend
dotnet restore
dotnet ef database update
dotnet run
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Docker Deployment

### Build and Run
```bash
docker-compose up -d
```

### Verify Services
```bash
docker-compose ps
```

### Logs
```bash
docker-compose logs -f api
docker-compose logs -f frontend
```

### Shutdown
```bash
docker-compose down
```

## Production Deployment

### Environment Configuration

Create `.env.production`:
```env
ASPNETCORE_ENVIRONMENT=Production
ConnectionStrings__DefaultConnection=<production_connection_string>
JwtSettings__Secret=<your_secret_key>
OPENAI_API_KEY=<your_openai_key>
```

### Backend Deployment

#### Using Azure
```bash
az login
dotnet publish -c Release -o ./publish
az webapp deployment source config-zip -g <resource-group> -n <app-name> --src <path-to-zip>
```

#### Using AWS
```bash
dotnet publish -c Release
aws elasticbeanstalk create-environment --application-name TimeX-API
```

#### Using Heroku
```bash
heroku login
git push heroku main
```

### Frontend Deployment

#### Using Vercel
```bash
npm install -g vercel
vercel
```

#### Using Netlify
```bash
npm install -g netlify-cli
netlify deploy
```

#### Using AWS S3 + CloudFront
```bash
npm run build
aws s3 sync dist/ s3://<bucket-name>
```

## Database Migrations

### Create Migration
```bash
cd backend
dotnet ef migrations add <migration-name>
```

### Apply Migration
```bash
dotnet ef database update
```

### Production Migration
```bash
dotnet ef database update --configuration Release
```

## SSL/TLS Configuration

### Generate Self-Signed Certificate
```bash
openssl req -new -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

### Configure in Nginx
```nginx
listen 443 ssl;
ssl_certificate /etc/nginx/ssl/cert.pem;
ssl_certificate_key /etc/nginx/ssl/key.pem;
```

## Backup Strategy

### Database Backup
```bash
# PostgreSQL dump
pg_dump -U postgres TimeXDB > backup.sql

# Restore from backup
psql -U postgres TimeXDB < backup.sql
```

### Automated Backups
```bash
# Schedule with cron
0 2 * * * pg_dump -U postgres TimeXDB > /backups/timex_$(date +\%Y\%m\%d).sql
```

## Monitoring and Logging

### Application Logging
```csharp
builder.Services.AddLogging(config => 
{
    config.AddConsole();
    config.AddFile("logs/app-{Date}.txt");
});
```

### Error Tracking
- Set up Sentry for error monitoring
- Configure application insights
- Monitor API response times

## Performance Optimization

### Database
- Enable query logging: `SET log_statement = 'all';`
- Monitor slow queries: `SET log_min_duration_statement = 1000;`
- Create indexes on frequently searched columns
- Analyze query plans with EXPLAIN

### API Caching
```csharp
services.AddResponseCaching();
```

### Frontend
- Enable gzip compression
- Use CDN for static assets
- Implement lazy loading
- Tree-shaking unused code

## Security Hardening

### API Security
```csharp
// Enable HTTPS redirect
app.UseHttpsRedirection();

// Add security headers
app.UseHsts();
```

### Database Security
- Use strong passwords
- Enable SSL connections
- Restrict network access
- Regular security patches

### Application Security
- Keep dependencies updated
- Use parameterized queries
- Implement input validation
- Enable CORS properly

## Scaling

### Horizontal Scaling
1. Deploy multiple API instances
2. Use load balancer (Nginx, HAProxy)
3. Implement session stickiness
4. Use distributed caching (Redis)

### Database Scaling
1. Set up read replicas
2. Implement connection pooling
3. Use query optimization
4. Archive old data

## Monitoring Checklist

- [ ] Application uptime monitoring
- [ ] Database performance monitoring
- [ ] Error rate tracking
- [ ] API response time monitoring
- [ ] Server resource usage
- [ ] Network latency
- [ ] User activity tracking
- [ ] Security alerts

## Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Test connection
psql -h localhost -U postgres -d TimeXDB
```

#### API Not Starting
```bash
# Check logs
docker-compose logs api

# Verify environment variables
docker-compose exec api env
```

#### Frontend Not Loading
```bash
# Clear build cache
rm -rf dist/
npm run build

# Check nginx config
docker-compose exec frontend nginx -t
```

## Rollback Procedure

### Code Rollback
```bash
git revert <commit-hash>
git push
# Redeploy
```

### Database Rollback
```bash
dotnet ef migrations remove
dotnet ef database update <previous-migration>
```

---

**Last Updated:** 2024
**Version:** 1.0.0
