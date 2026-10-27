using TimeX.Data.Entities;
using BCrypt.Net;

namespace TimeX.Data;

/// <summary>
/// Seeder for initial database data
/// </summary>
public class DatabaseSeeder
{
    public static async Task SeedAsync(TimeXDbContext context)
    {
        try
        {
            // Check if data already exists
            if (context.Categories.Any())
                return;

            // Create categories
            var categories = new[]
            {
                new Category { Id = Guid.NewGuid(), Name = "Luxury Watches", Description = "Premium and luxury timepieces" },
                new Category { Id = Guid.NewGuid(), Name = "Sports Watches", Description = "Durable watches for sports enthusiasts" },
                new Category { Id = Guid.NewGuid(), Name = "Dress Watches", Description = "Elegant watches for formal occasions" },
                new Category { Id = Guid.NewGuid(), Name = "Casual Watches", Description = "Everyday casual timepieces" },
                new Category { Id = Guid.NewGuid(), Name = "Dive Watches", Description = "Professional diving watches" }
            };

            await context.Categories.AddRangeAsync(categories);
            await context.SaveChangesAsync();

            // Create admin user
            var adminPassword = "Admin@123";
            var adminUser = new User
            {
                Id = Guid.NewGuid(),
                Email = "admin@timex.local",
                PasswordHash = BCrypt.HashPassword(adminPassword),
                FirstName = "Admin",
                LastName = "User",
                Role = UserRole.Admin,
                IsActive = true
            };

            // Create customer users
            var customerUsers = new[]
            {
                new User
                {
                    Id = Guid.NewGuid(),
                    Email = "customer1@example.com",
                    PasswordHash = BCrypt.HashPassword("Customer@123"),
                    FirstName = "John",
                    LastName = "Doe",
                    Role = UserRole.Customer,
                    IsActive = true,
                    Address = "123 Main St",
                    City = "New York",
                    PostalCode = "10001",
                    Country = "USA"
                },
                new User
                {
                    Id = Guid.NewGuid(),
                    Email = "customer2@example.com",
                    PasswordHash = BCrypt.HashPassword("Customer@123"),
                    FirstName = "Jane",
                    LastName = "Smith",
                    Role = UserRole.Customer,
                    IsActive = true,
                    Address = "456 Oak Ave",
                    City = "Los Angeles",
                    PostalCode = "90001",
                    Country = "USA"
                }
            };

            await context.Users.AddAsync(adminUser);
            await context.Users.AddRangeAsync(customerUsers);
            await context.SaveChangesAsync();

            // Create sample products
            var luxuryCategory = categories[0];
            var sportsCategory = categories[1];

            var products = new[]
            {
                new Product
                {
                    Id = Guid.NewGuid(),
                    Name = "Rolex Submariner",
                    Description = "Iconic luxury dive watch with exceptional precision",
                    Sku = "ROLEX-SUB-001",
                    Price = 9500.00m,
                    Brand = "Rolex",
                    CategoryId = luxuryCategory.Id,
                    Model = "116610LN",
                    WaterResistance = "300m",
                    Material = "Stainless Steel",
                    Movement = "Automatic",
                    Diameter = "40mm",
                    Color = "Black",
                    IsActive = true,
                    ImageUrl = "/images/rolex-submariner.jpg"
                },
                new Product
                {
                    Id = Guid.NewGuid(),
                    Name = "Omega Seamaster",
                    Description = "Professional sea watch with Swiss precision",
                    Sku = "OMEGA-SEA-001",
                    Price = 6500.00m,
                    Brand = "Omega",
                    CategoryId = luxuryCategory.Id,
                    Model = "2210.50.00",
                    WaterResistance = "300m",
                    Material = "Stainless Steel",
                    Movement = "Automatic",
                    Diameter = "42mm",
                    Color = "Blue",
                    IsActive = true,
                    ImageUrl = "/images/omega-seamaster.jpg"
                },
                new Product
                {
                    Id = Guid.NewGuid(),
                    Name = "Tag Heuer Carrera",
                    Description = "Racing inspired chronograph with superior performance",
                    Sku = "TAG-CAR-001",
                    Price = 4200.00m,
                    Brand = "Tag Heuer",
                    CategoryId = sportsCategory.Id,
                    Model = "CV2A10.BA0796",
                    WaterResistance = "100m",
                    Material = "Stainless Steel",
                    Movement = "Automatic",
                    Diameter = "41mm",
                    Color = "Black",
                    IsActive = true,
                    ImageUrl = "/images/tag-carrera.jpg"
                },
                new Product
                {
                    Id = Guid.NewGuid(),
                    Name = "Seiko Prospex",
                    Description = "Adventure-ready sports watch by Seiko",
                    Sku = "SEIKO-PROS-001",
                    Price = 1200.00m,
                    Brand = "Seiko",
                    CategoryId = sportsCategory.Id,
                    Model = "SBDC055",
                    WaterResistance = "200m",
                    Material = "Stainless Steel",
                    Movement = "Automatic",
                    Diameter = "42mm",
                    Color = "Black",
                    IsActive = true,
                    ImageUrl = "/images/seiko-prospex.jpg"
                },
                new Product
                {
                    Id = Guid.NewGuid(),
                    Name = "Cartier Tank",
                    Description = "Timeless dress watch with iconic design",
                    Sku = "CARTIER-TANK-001",
                    Price = 3800.00m,
                    Brand = "Cartier",
                    CategoryId = categories[2].Id,
                    Model = "W5200014",
                    WaterResistance = "30m",
                    Material = "18K Gold",
                    Movement = "Quartz",
                    Diameter = "33mm",
                    Color = "Gold",
                    IsActive = true,
                    ImageUrl = "/images/cartier-tank.jpg"
                }
            };

            await context.Products.AddRangeAsync(products);
            await context.SaveChangesAsync();

            // Create inventory for products
            var inventoryItems = products.Select(p => new Inventory
            {
                Id = Guid.NewGuid(),
                ProductId = p.Id,
                Quantity = 50,
                ReservedQuantity = 0,
                MinimumStockLevel = 5,
                WarehouseLocation = "WH-A-01"
            }).ToArray();

            await context.Inventory.AddRangeAsync(inventoryItems);
            await context.SaveChangesAsync();

            // Create sample reviews
            var reviews = new[]
            {
                new Review
                {
                    Id = Guid.NewGuid(),
                    ProductId = products[0].Id,
                    UserId = customerUsers[0].Id,
                    Rating = 5,
                    Title = "Excellent luxury watch",
                    Comment = "Amazing craftsmanship and precision. Highly recommended!",
                    IsVerifiedPurchase = true,
                    HelpfulCount = 15
                },
                new Review
                {
                    Id = Guid.NewGuid(),
                    ProductId = products[0].Id,
                    UserId = customerUsers[1].Id,
                    Rating = 5,
                    Title = "Worth every penny",
                    Comment = "Beautiful watch, accurate and durable. Perfect investment.",
                    IsVerifiedPurchase = true,
                    HelpfulCount = 8
                }
            };

            await context.Reviews.AddRangeAsync(reviews);
            await context.SaveChangesAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error seeding database: {ex.Message}");
            throw;
        }
    }
}
