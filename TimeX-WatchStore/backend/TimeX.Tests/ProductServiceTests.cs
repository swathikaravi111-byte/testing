using Xunit;
using TimeX.Business.Services;
using TimeX.Data;
using TimeX.Data.Entities;
using Microsoft.EntityFrameworkCore;

namespace TimeX.Tests;

public class ProductServiceTests
{
    private readonly TimeXDbContext _context;
    private readonly ProductService _productService;

    public ProductServiceTests()
    {
        var options = new DbContextOptionsBuilder<TimeXDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new TimeXDbContext(options);
        _productService = new ProductService(_context);
    }

    [Fact]
    public async Task GetAllProductsAsync_ShouldReturnAllActiveProducts()
    {
        // Arrange
        var category = new Category { Name = "Luxury" };
        _context.Categories.Add(category);
        await _context.SaveChangesAsync();

        var products = new[]
        {
            new Product { Name = "Watch 1", CategoryId = category.Id, Price = 1000, Sku = "SKU1", Brand = "Brand1", IsActive = true },
            new Product { Name = "Watch 2", CategoryId = category.Id, Price = 2000, Sku = "SKU2", Brand = "Brand2", IsActive = true },
            new Product { Name = "Watch 3", CategoryId = category.Id, Price = 3000, Sku = "SKU3", Brand = "Brand3", IsActive = false }
        };
        _context.Products.AddRange(products);
        await _context.SaveChangesAsync();

        // Act
        var result = await _productService.GetAllProductsAsync();

        // Assert
        Assert.Equal(2, result.Count());
    }

    [Fact]
    public async Task GetProductByIdAsync_WithValidId_ShouldReturnProduct()
    {
        // Arrange
        var category = new Category { Name = "Luxury" };
        _context.Categories.Add(category);
        await _context.SaveChangesAsync();

        var product = new Product
        {
            Name = "Test Watch",
            CategoryId = category.Id,
            Price = 1000,
            Sku = "TEST-SKU",
            Brand = "TestBrand",
            IsActive = true
        };
        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        // Act
        var result = await _productService.GetProductByIdAsync(product.Id);

        // Assert
        Assert.NotNull(result);
        Assert.Equal("Test Watch", result.Name);
    }

    [Fact]
    public async Task SearchProductsAsync_ShouldReturnMatchingProducts()
    {
        // Arrange
        var category = new Category { Name = "Luxury" };
        _context.Categories.Add(category);
        await _context.SaveChangesAsync();

        var products = new[]
        {
            new Product { Name = "Rolex Submariner", CategoryId = category.Id, Price = 1000, Sku = "ROLEX1", Brand = "Rolex", IsActive = true },
            new Product { Name = "Omega Seamaster", CategoryId = category.Id, Price = 2000, Sku = "OMEGA1", Brand = "Omega", IsActive = true }
        };
        _context.Products.AddRange(products);
        await _context.SaveChangesAsync();

        // Act
        var result = await _productService.SearchProductsAsync("Rolex");

        // Assert
        Assert.Single(result);
        Assert.Contains("Rolex", result.First().Name);
    }

    [Fact]
    public async Task CreateProductAsync_ShouldAddNewProduct()
    {
        // Arrange
        var category = new Category { Name = "Luxury" };
        _context.Categories.Add(category);
        await _context.SaveChangesAsync();

        var createDto = new CreateProductDto
        {
            Name = "New Watch",
            Sku = "NEW-WATCH",
            Price = 5000,
            Brand = "NewBrand",
            CategoryId = category.Id,
            Description = "Test",
            Model = "Model1",
            WaterResistance = "100m",
            Material = "Gold",
            Movement = "Automatic",
            Diameter = "42mm",
            Color = "Black"
        };

        // Act
        var result = await _productService.CreateProductAsync(createDto);

        // Assert
        Assert.NotEqual(Guid.Empty, result.Id);
        Assert.Equal("New Watch", result.Name);
        var savedProduct = await _context.Products.FindAsync(result.Id);
        Assert.NotNull(savedProduct);
    }
}
