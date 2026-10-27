using TimeX.Data;
using TimeX.Data.Entities;
using Microsoft.EntityFrameworkCore;

namespace TimeX.Business.Services;

public interface IProductService
{
    Task<IEnumerable<ProductDto>> GetAllProductsAsync();
    Task<ProductDto?> GetProductByIdAsync(Guid id);
    Task<IEnumerable<ProductDto>> GetProductsByCategoryAsync(Guid categoryId);
    Task<IEnumerable<ProductDto>> SearchProductsAsync(string query);
    Task<IEnumerable<ProductDto>> FilterProductsAsync(ProductFilterDto filter);
    Task<ProductDto> CreateProductAsync(CreateProductDto dto);
    Task<ProductDto> UpdateProductAsync(Guid id, UpdateProductDto dto);
    Task<bool> DeleteProductAsync(Guid id);
}

public class ProductService : IProductService
{
    private readonly TimeXDbContext _context;

    public ProductService(TimeXDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<ProductDto>> GetAllProductsAsync()
    {
        var products = await _context.Products
            .Where(p => p.IsActive)
            .Include(p => p.Category)
            .Include(p => p.Reviews)
            .ToListAsync();

        return products.Select(MapToDto).ToList();
    }

    public async Task<ProductDto?> GetProductByIdAsync(Guid id)
    {
        var product = await _context.Products
            .Include(p => p.Category)
            .Include(p => p.Reviews)
            .Include(p => p.Inventory)
            .FirstOrDefaultAsync(p => p.Id == id);

        return product == null ? null : MapToDto(product);
    }

    public async Task<IEnumerable<ProductDto>> GetProductsByCategoryAsync(Guid categoryId)
    {
        var products = await _context.Products
            .Where(p => p.CategoryId == categoryId && p.IsActive)
            .Include(p => p.Category)
            .Include(p => p.Reviews)
            .ToListAsync();

        return products.Select(MapToDto).ToList();
    }

    public async Task<IEnumerable<ProductDto>> SearchProductsAsync(string query)
    {
        var products = await _context.Products
            .Where(p => p.IsActive && (
                p.Name.Contains(query) ||
                p.Description.Contains(query) ||
                p.Brand.Contains(query) ||
                p.Model.Contains(query)))
            .Include(p => p.Category)
            .Include(p => p.Reviews)
            .ToListAsync();

        return products.Select(MapToDto).ToList();
    }

    public async Task<IEnumerable<ProductDto>> FilterProductsAsync(ProductFilterDto filter)
    {
        var query = _context.Products.Where(p => p.IsActive);

        if (!string.IsNullOrEmpty(filter.Brand))
            query = query.Where(p => p.Brand == filter.Brand);

        if (filter.MinPrice.HasValue)
            query = query.Where(p => p.Price >= filter.MinPrice.Value);

        if (filter.MaxPrice.HasValue)
            query = query.Where(p => p.Price <= filter.MaxPrice.Value);

        if (filter.CategoryId.HasValue)
            query = query.Where(p => p.CategoryId == filter.CategoryId.Value);

        if (!string.IsNullOrEmpty(filter.Material))
            query = query.Where(p => p.Material == filter.Material);

        var products = await query
            .Include(p => p.Category)
            .Include(p => p.Reviews)
            .ToListAsync();

        return products.Select(MapToDto).ToList();
    }

    public async Task<ProductDto> CreateProductAsync(CreateProductDto dto)
    {
        var product = new Product
        {
            Name = dto.Name,
            Description = dto.Description,
            Sku = dto.Sku,
            Price = dto.Price,
            DiscountPrice = dto.DiscountPrice,
            Brand = dto.Brand,
            CategoryId = dto.CategoryId,
            Model = dto.Model,
            WaterResistance = dto.WaterResistance,
            Material = dto.Material,
            Movement = dto.Movement,
            Diameter = dto.Diameter,
            Color = dto.Color,
            ImageUrl = dto.ImageUrl,
            IsActive = true
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync();

        return MapToDto(product);
    }

    public async Task<ProductDto> UpdateProductAsync(Guid id, UpdateProductDto dto)
    {
        var product = await _context.Products.FindAsync(id);
        if (product == null)
            throw new Exception("Product not found");

        product.Name = dto.Name ?? product.Name;
        product.Description = dto.Description ?? product.Description;
        product.Price = dto.Price ?? product.Price;
        product.DiscountPrice = dto.DiscountPrice ?? product.DiscountPrice;
        product.Brand = dto.Brand ?? product.Brand;
        product.Color = dto.Color ?? product.Color;
        product.ImageUrl = dto.ImageUrl ?? product.ImageUrl;
        product.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();
        await _context.Entry(product).ReloadAsync();
        await _context.Entry(product).Collection(p => p.Reviews).LoadAsync();

        return MapToDto(product);
    }

    public async Task<bool> DeleteProductAsync(Guid id)
    {
        var product = await _context.Products.FindAsync(id);
        if (product == null)
            return false;

        product.IsActive = false;
        await _context.SaveChangesAsync();
        return true;
    }

    private static ProductDto MapToDto(Product product)
    {
        return new ProductDto
        {
            Id = product.Id,
            Name = product.Name,
            Description = product.Description,
            Sku = product.Sku,
            Price = product.Price,
            DiscountPrice = product.DiscountPrice,
            Brand = product.Brand,
            Category = product.Category?.Name ?? string.Empty,
            Model = product.Model,
            WaterResistance = product.WaterResistance,
            Material = product.Material,
            Movement = product.Movement,
            Diameter = product.Diameter,
            Color = product.Color,
            AverageRating = product.AverageRating,
            TotalReviews = product.TotalReviews,
            ImageUrl = product.ImageUrl
        };
    }
}

public class ProductDto
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string Sku { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public decimal? DiscountPrice { get; set; }
    public string Brand { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public string Model { get; set; } = string.Empty;
    public string WaterResistance { get; set; } = string.Empty;
    public string Material { get; set; } = string.Empty;
    public string Movement { get; set; } = string.Empty;
    public string Diameter { get; set; } = string.Empty;
    public string Color { get; set; } = string.Empty;
    public decimal AverageRating { get; set; }
    public int TotalReviews { get; set; }
    public string? ImageUrl { get; set; }
}

public class CreateProductDto
{
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string Sku { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public decimal? DiscountPrice { get; set; }
    public string Brand { get; set; } = string.Empty;
    public Guid CategoryId { get; set; }
    public string Model { get; set; } = string.Empty;
    public string WaterResistance { get; set; } = string.Empty;
    public string Material { get; set; } = string.Empty;
    public string Movement { get; set; } = string.Empty;
    public string Diameter { get; set; } = string.Empty;
    public string Color { get; set; } = string.Empty;
    public string? ImageUrl { get; set; }
}

public class UpdateProductDto
{
    public string? Name { get; set; }
    public string? Description { get; set; }
    public decimal? Price { get; set; }
    public decimal? DiscountPrice { get; set; }
    public string? Brand { get; set; }
    public string? Color { get; set; }
    public string? ImageUrl { get; set; }
}

public class ProductFilterDto
{
    public string? Brand { get; set; }
    public decimal? MinPrice { get; set; }
    public decimal? MaxPrice { get; set; }
    public Guid? CategoryId { get; set; }
    public string? Material { get; set; }
}
