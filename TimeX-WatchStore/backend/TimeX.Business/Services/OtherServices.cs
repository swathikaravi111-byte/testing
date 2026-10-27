using TimeX.Data;
using TimeX.Data.Entities;
using Microsoft.EntityFrameworkCore;

namespace TimeX.Business.Services;

// ============= CART SERVICE =============
public interface ICartService
{
    Task<CartDto> GetCartAsync(Guid userId);
    Task<CartItemDto> AddToCartAsync(Guid userId, Guid productId, int quantity);
    Task<CartItemDto> UpdateCartItemAsync(Guid itemId, int quantity);
    Task<bool> RemoveFromCartAsync(Guid itemId);
    Task<bool> ClearCartAsync(Guid userId);
}

public class CartService : ICartService
{
    private readonly TimeXDbContext _context;

    public CartService(TimeXDbContext context) => _context = context;

    public async Task<CartDto> GetCartAsync(Guid userId)
    {
        var items = await _context.CartItems
            .Where(c => c.UserId == userId)
            .Include(c => c.Product)
            .ToListAsync();

        var total = items.Sum(i => i.UnitPrice * i.Quantity);

        return new CartDto
        {
            UserId = userId,
            Items = items.Select(i => new CartItemDto
            {
                Id = i.Id,
                ProductId = i.ProductId,
                ProductName = i.Product?.Name ?? string.Empty,
                Quantity = i.Quantity,
                UnitPrice = i.UnitPrice,
                TotalPrice = i.UnitPrice * i.Quantity
            }).ToList(),
            TotalPrice = total
        };
    }

    public async Task<CartItemDto> AddToCartAsync(Guid userId, Guid productId, int quantity)
    {
        var existingItem = await _context.CartItems
            .FirstOrDefaultAsync(c => c.UserId == userId && c.ProductId == productId);

        if (existingItem != null)
        {
            existingItem.Quantity += quantity;
            existingItem.UpdatedAt = DateTime.UtcNow;
        }
        else
        {
            var product = await _context.Products.FindAsync(productId);
            if (product == null)
                throw new Exception("Product not found");

            existingItem = new CartItem
            {
                UserId = userId,
                ProductId = productId,
                Quantity = quantity,
                UnitPrice = product.Price
            };
            _context.CartItems.Add(existingItem);
        }

        await _context.SaveChangesAsync();

        var product2 = await _context.Products.FindAsync(productId);
        return new CartItemDto
        {
            Id = existingItem.Id,
            ProductId = productId,
            ProductName = product2?.Name ?? string.Empty,
            Quantity = existingItem.Quantity,
            UnitPrice = existingItem.UnitPrice,
            TotalPrice = existingItem.UnitPrice * existingItem.Quantity
        };
    }

    public async Task<CartItemDto> UpdateCartItemAsync(Guid itemId, int quantity)
    {
        var item = await _context.CartItems.Include(c => c.Product).FirstOrDefaultAsync(c => c.Id == itemId);
        if (item == null)
            throw new Exception("Cart item not found");

        item.Quantity = quantity;
        item.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        return new CartItemDto
        {
            Id = item.Id,
            ProductId = item.ProductId,
            ProductName = item.Product?.Name ?? string.Empty,
            Quantity = item.Quantity,
            UnitPrice = item.UnitPrice,
            TotalPrice = item.UnitPrice * item.Quantity
        };
    }

    public async Task<bool> RemoveFromCartAsync(Guid itemId)
    {
        var item = await _context.CartItems.FindAsync(itemId);
        if (item == null)
            return false;

        _context.CartItems.Remove(item);
        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<bool> ClearCartAsync(Guid userId)
    {
        var items = await _context.CartItems.Where(c => c.UserId == userId).ToListAsync();
        _context.CartItems.RemoveRange(items);
        await _context.SaveChangesAsync();
        return true;
    }
}

public class CartDto
{
    public Guid UserId { get; set; }
    public List<CartItemDto> Items { get; set; } = [];
    public decimal TotalPrice { get; set; }
}

public class CartItemDto
{
    public Guid Id { get; set; }
    public Guid ProductId { get; set; }
    public string ProductName { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal TotalPrice { get; set; }
}

// ============= ORDER SERVICE =============
public interface IOrderService
{
    Task<OrderDto> GetOrderByIdAsync(Guid id);
    Task<IEnumerable<OrderDto>> GetUserOrdersAsync(Guid userId);
    Task<IEnumerable<OrderDto>> GetAllOrdersAsync();
    Task<OrderDto> CreateOrderAsync(Guid userId, CreateOrderDto dto);
    Task<OrderDto> UpdateOrderStatusAsync(Guid id, OrderStatus status);
}

public class OrderService : IOrderService
{
    private readonly TimeXDbContext _context;

    public OrderService(TimeXDbContext context) => _context = context;

    public async Task<OrderDto> GetOrderByIdAsync(Guid id)
    {
        var order = await _context.Orders
            .Include(o => o.OrderItems).ThenInclude(oi => oi.Product)
            .FirstOrDefaultAsync(o => o.Id == id);

        return order == null ? throw new Exception("Order not found") : MapToDto(order);
    }

    public async Task<IEnumerable<OrderDto>> GetUserOrdersAsync(Guid userId)
    {
        var orders = await _context.Orders
            .Where(o => o.UserId == userId)
            .Include(o => o.OrderItems).ThenInclude(oi => oi.Product)
            .OrderByDescending(o => o.CreatedAt)
            .ToListAsync();

        return orders.Select(MapToDto).ToList();
    }

    public async Task<IEnumerable<OrderDto>> GetAllOrdersAsync()
    {
        var orders = await _context.Orders
            .Include(o => o.OrderItems).ThenInclude(oi => oi.Product)
            .OrderByDescending(o => o.CreatedAt)
            .ToListAsync();

        return orders.Select(MapToDto).ToList();
    }

    public async Task<OrderDto> CreateOrderAsync(Guid userId, CreateOrderDto dto)
    {
        using var transaction = await _context.Database.BeginTransactionAsync();
        try
        {
            var cartItems = await _context.CartItems
                .Include(c => c.Product)
                .Where(c => c.UserId == userId)
                .ToListAsync();

            if (!cartItems.Any())
                throw new Exception("Cart is empty");

            var order = new Order
            {
                OrderNumber = $"ORD-{DateTime.UtcNow:yyyyMMddHHmmss}-{Guid.NewGuid().ToString().Substring(0, 8)}",
                UserId = userId,
                Status = OrderStatus.Pending,
                TotalAmount = cartItems.Sum(c => c.UnitPrice * c.Quantity),
                TaxAmount = cartItems.Sum(c => c.UnitPrice * c.Quantity) * 0.1m,
                ShippingCost = dto.ShippingCost ?? 10m,
                ShippingAddress = dto.ShippingAddress,
                BillingAddress = dto.BillingAddress,
                ShippingMethod = dto.ShippingMethod
            };

            _context.Orders.Add(order);

            foreach (var cartItem in cartItems)
            {
                _context.OrderItems.Add(new OrderItem
                {
                    OrderId = order.Id,
                    ProductId = cartItem.ProductId,
                    Quantity = cartItem.Quantity,
                    UnitPrice = cartItem.UnitPrice,
                    TotalPrice = cartItem.UnitPrice * cartItem.Quantity
                });

                // Update inventory
                var inventory = await _context.Inventory.FirstOrDefaultAsync(i => i.ProductId == cartItem.ProductId);
                if (inventory != null)
                {
                    inventory.ReservedQuantity += cartItem.Quantity;
                }
            }

            _context.CartItems.RemoveRange(cartItems);
            await _context.SaveChangesAsync();
            await transaction.CommitAsync();

            return MapToDto(order);
        }
        catch
        {
            await transaction.RollbackAsync();
            throw;
        }
    }

    public async Task<OrderDto> UpdateOrderStatusAsync(Guid id, OrderStatus status)
    {
        var order = await _context.Orders.FindAsync(id);
        if (order == null)
            throw new Exception("Order not found");

        order.Status = status;
        if (status == OrderStatus.Shipped)
            order.ShippedAt = DateTime.UtcNow;
        if (status == OrderStatus.Delivered)
            order.DeliveredAt = DateTime.UtcNow;

        order.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();
        await _context.Entry(order).Collection(o => o.OrderItems).LoadAsync();

        return MapToDto(order);
    }

    private static OrderDto MapToDto(Order order)
    {
        return new OrderDto
        {
            Id = order.Id,
            OrderNumber = order.OrderNumber,
            Status = order.Status.ToString(),
            TotalAmount = order.TotalAmount,
            TaxAmount = order.TaxAmount,
            ShippingCost = order.ShippingCost,
            ShippingAddress = order.ShippingAddress,
            CreatedAt = order.CreatedAt,
            Items = order.OrderItems.Select(oi => new OrderItemDto
            {
                ProductId = oi.ProductId,
                ProductName = oi.Product?.Name ?? string.Empty,
                Quantity = oi.Quantity,
                UnitPrice = oi.UnitPrice,
                TotalPrice = oi.TotalPrice
            }).ToList()
        };
    }
}

public class OrderDto
{
    public Guid Id { get; set; }
    public string OrderNumber { get; set; } = string.Empty;
    public string Status { get; set; } = string.Empty;
    public decimal TotalAmount { get; set; }
    public decimal TaxAmount { get; set; }
    public decimal ShippingCost { get; set; }
    public string ShippingAddress { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
    public List<OrderItemDto> Items { get; set; } = [];
}

public class OrderItemDto
{
    public Guid ProductId { get; set; }
    public string ProductName { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal TotalPrice { get; set; }
}

public class CreateOrderDto
{
    public string ShippingAddress { get; set; } = string.Empty;
    public string BillingAddress { get; set; } = string.Empty;
    public string ShippingMethod { get; set; } = string.Empty;
    public decimal? ShippingCost { get; set; }
}

// ============= USER SERVICE =============
public interface IUserService
{
    Task<UserProfileDto> GetUserProfileAsync(Guid userId);
    Task<UserProfileDto> UpdateUserProfileAsync(Guid userId, UpdateUserProfileDto dto);
}

public class UserService : IUserService
{
    private readonly TimeXDbContext _context;

    public UserService(TimeXDbContext context) => _context = context;

    public async Task<UserProfileDto> GetUserProfileAsync(Guid userId)
    {
        var user = await _context.Users.FindAsync(userId);
        if (user == null)
            throw new Exception("User not found");

        return new UserProfileDto
        {
            Id = user.Id,
            Email = user.Email,
            FirstName = user.FirstName,
            LastName = user.LastName,
            PhoneNumber = user.PhoneNumber,
            Address = user.Address,
            City = user.City,
            PostalCode = user.PostalCode,
            Country = user.Country
        };
    }

    public async Task<UserProfileDto> UpdateUserProfileAsync(Guid userId, UpdateUserProfileDto dto)
    {
        var user = await _context.Users.FindAsync(userId);
        if (user == null)
            throw new Exception("User not found");

        user.FirstName = dto.FirstName ?? user.FirstName;
        user.LastName = dto.LastName ?? user.LastName;
        user.PhoneNumber = dto.PhoneNumber ?? user.PhoneNumber;
        user.Address = dto.Address ?? user.Address;
        user.City = dto.City ?? user.City;
        user.PostalCode = dto.PostalCode ?? user.PostalCode;
        user.Country = dto.Country ?? user.Country;
        user.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();

        return new UserProfileDto
        {
            Id = user.Id,
            Email = user.Email,
            FirstName = user.FirstName,
            LastName = user.LastName,
            PhoneNumber = user.PhoneNumber,
            Address = user.Address,
            City = user.City,
            PostalCode = user.PostalCode,
            Country = user.Country
        };
    }
}

public class UserProfileDto
{
    public Guid Id { get; set; }
    public string Email { get; set; } = string.Empty;
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public string PhoneNumber { get; set; } = string.Empty;
    public string Address { get; set; } = string.Empty;
    public string City { get; set; } = string.Empty;
    public string PostalCode { get; set; } = string.Empty;
    public string Country { get; set; } = string.Empty;
}

public class UpdateUserProfileDto
{
    public string? FirstName { get; set; }
    public string? LastName { get; set; }
    public string? PhoneNumber { get; set; }
    public string? Address { get; set; }
    public string? City { get; set; }
    public string? PostalCode { get; set; }
    public string? Country { get; set; }
}

// ============= WISHLIST SERVICE =============
public interface IWishlistService
{
    Task<WishlistDto> GetWishlistAsync(Guid userId);
    Task<bool> AddToWishlistAsync(Guid userId, Guid productId);
    Task<bool> RemoveFromWishlistAsync(Guid userId, Guid productId);
}

public class WishlistService : IWishlistService
{
    private readonly TimeXDbContext _context;

    public WishlistService(TimeXDbContext context) => _context = context;

    public async Task<WishlistDto> GetWishlistAsync(Guid userId)
    {
        var items = await _context.WishlistItems
            .Where(w => w.UserId == userId)
            .Include(w => w.Product)
            .ToListAsync();

        return new WishlistDto
        {
            UserId = userId,
            Items = items.Select(i => new WishlistItemDto
            {
                ProductId = i.ProductId,
                ProductName = i.Product?.Name ?? string.Empty,
                Price = i.Product?.Price ?? 0,
                ImageUrl = i.Product?.ImageUrl
            }).ToList()
        };
    }

    public async Task<bool> AddToWishlistAsync(Guid userId, Guid productId)
    {
        var exists = await _context.WishlistItems
            .AnyAsync(w => w.UserId == userId && w.ProductId == productId);

        if (!exists)
        {
            _context.WishlistItems.Add(new WishlistItem { UserId = userId, ProductId = productId });
            await _context.SaveChangesAsync();
        }
        return true;
    }

    public async Task<bool> RemoveFromWishlistAsync(Guid userId, Guid productId)
    {
        var item = await _context.WishlistItems
            .FirstOrDefaultAsync(w => w.UserId == userId && w.ProductId == productId);

        if (item != null)
        {
            _context.WishlistItems.Remove(item);
            await _context.SaveChangesAsync();
        }
        return true;
    }
}

public class WishlistDto
{
    public Guid UserId { get; set; }
    public List<WishlistItemDto> Items { get; set; } = [];
}

public class WishlistItemDto
{
    public Guid ProductId { get; set; }
    public string ProductName { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? ImageUrl { get; set; }
}

// ============= REVIEW SERVICE =============
public interface IReviewService
{
    Task<IEnumerable<ReviewDto>> GetProductReviewsAsync(Guid productId);
    Task<ReviewDto> CreateReviewAsync(CreateReviewDto dto);
    Task<ReviewDto> UpdateReviewAsync(Guid id, UpdateReviewDto dto);
    Task<bool> DeleteReviewAsync(Guid id);
}

public class ReviewService : IReviewService
{
    private readonly TimeXDbContext _context;

    public ReviewService(TimeXDbContext context) => _context = context;

    public async Task<IEnumerable<ReviewDto>> GetProductReviewsAsync(Guid productId)
    {
        var reviews = await _context.Reviews
            .Where(r => r.ProductId == productId)
            .Include(r => r.User)
            .OrderByDescending(r => r.CreatedAt)
            .ToListAsync();

        return reviews.Select(r => new ReviewDto
        {
            Id = r.Id,
            Rating = r.Rating,
            Title = r.Title,
            Comment = r.Comment,
            UserName = $"{r.User?.FirstName} {r.User?.LastName}",
            CreatedAt = r.CreatedAt
        }).ToList();
    }

    public async Task<ReviewDto> CreateReviewAsync(CreateReviewDto dto)
    {
        var review = new Review
        {
            ProductId = dto.ProductId,
            UserId = dto.UserId,
            Rating = dto.Rating,
            Title = dto.Title,
            Comment = dto.Comment,
            IsVerifiedPurchase = true
        };

        _context.Reviews.Add(review);
        await _context.SaveChangesAsync();

        // Update product rating
        await UpdateProductRating(dto.ProductId);

        return new ReviewDto
        {
            Id = review.Id,
            Rating = review.Rating,
            Title = review.Title,
            Comment = review.Comment
        };
    }

    public async Task<ReviewDto> UpdateReviewAsync(Guid id, UpdateReviewDto dto)
    {
        var review = await _context.Reviews.FindAsync(id);
        if (review == null)
            throw new Exception("Review not found");

        var oldRating = review.Rating;
        review.Rating = dto.Rating ?? review.Rating;
        review.Title = dto.Title ?? review.Title;
        review.Comment = dto.Comment ?? review.Comment;
        review.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();

        if (oldRating != review.Rating)
            await UpdateProductRating(review.ProductId);

        return new ReviewDto
        {
            Id = review.Id,
            Rating = review.Rating,
            Title = review.Title,
            Comment = review.Comment
        };
    }

    public async Task<bool> DeleteReviewAsync(Guid id)
    {
        var review = await _context.Reviews.FindAsync(id);
        if (review == null)
            return false;

        _context.Reviews.Remove(review);
        await _context.SaveChangesAsync();
        await UpdateProductRating(review.ProductId);
        return true;
    }

    private async Task UpdateProductRating(Guid productId)
    {
        var reviews = await _context.Reviews.Where(r => r.ProductId == productId).ToListAsync();
        var product = await _context.Products.FindAsync(productId);

        if (product != null)
        {
            product.AverageRating = reviews.Any() ? (decimal)reviews.Average(r => r.Rating) : 0;
            product.TotalReviews = reviews.Count;
            await _context.SaveChangesAsync();
        }
    }
}

public class ReviewDto
{
    public Guid Id { get; set; }
    public int Rating { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Comment { get; set; } = string.Empty;
    public string UserName { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}

public class CreateReviewDto
{
    public Guid ProductId { get; set; }
    public Guid UserId { get; set; }
    public int Rating { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Comment { get; set; } = string.Empty;
}

public class UpdateReviewDto
{
    public int? Rating { get; set; }
    public string? Title { get; set; }
    public string? Comment { get; set; }
}

// ============= INVENTORY SERVICE =============
public interface IInventoryService
{
    Task<InventoryDto> GetInventoryAsync(Guid productId);
    Task<bool> UpdateInventoryAsync(Guid productId, int quantity);
}

public class InventoryService : IInventoryService
{
    private readonly TimeXDbContext _context;

    public InventoryService(TimeXDbContext context) => _context = context;

    public async Task<InventoryDto> GetInventoryAsync(Guid productId)
    {
        var inventory = await _context.Inventory.FirstOrDefaultAsync(i => i.ProductId == productId);
        if (inventory == null)
            throw new Exception("Inventory not found");

        return new InventoryDto
        {
            ProductId = inventory.ProductId,
            Quantity = inventory.Quantity,
            ReservedQuantity = inventory.ReservedQuantity,
            AvailableQuantity = inventory.AvailableQuantity
        };
    }

    public async Task<bool> UpdateInventoryAsync(Guid productId, int quantity)
    {
        var inventory = await _context.Inventory.FirstOrDefaultAsync(i => i.ProductId == productId);
        if (inventory == null)
            return false;

        inventory.Quantity = quantity;
        inventory.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();
        return true;
    }
}

public class InventoryDto
{
    public Guid ProductId { get; set; }
    public int Quantity { get; set; }
    public int ReservedQuantity { get; set; }
    public int AvailableQuantity { get; set; }
}

// ============= CHATBOT SERVICE =============
public interface IChatbotService
{
    Task<ChatResponseDto> SendMessageAsync(Guid userId, string message);
}

public class ChatbotService : IChatbotService
{
    private readonly TimeXDbContext _context;

    public ChatbotService(TimeXDbContext context) => _context = context;

    public async Task<ChatResponseDto> SendMessageAsync(Guid userId, string message)
    {
        var response = await GenerateChatbotResponse(message);

        var chatMessage = new ChatMessage
        {
            UserId = userId,
            UserMessage = message,
            BotResponse = response,
            MessageType = ChatMessageType.General
        };

        _context.ChatMessages.Add(chatMessage);
        await _context.SaveChangesAsync();

        return new ChatResponseDto { Response = response };
    }

    private Task<string> GenerateChatbotResponse(string userMessage)
    {
        // Placeholder for AI integration
        var response = userMessage.ToLower() switch
        {
            var s when s.Contains("recommend") => "I'd be happy to recommend a watch! Tell me your budget and style preference.",
            var s when s.Contains("price") => "We have watches ranging from $500 to $50,000. What's your budget?",
            var s when s.Contains("luxury") => "Our luxury collection includes Rolex, Omega, and Cartier. Would you like details?",
            var s when s.Contains("sports") => "For sports watches, I recommend Tag Heuer or Seiko Prospex series.",
            _ => "Thank you for your interest! How can I help you find the perfect watch today?"
        };

        return Task.FromResult(response);
    }
}

public class ChatResponseDto
{
    public string Response { get; set; } = string.Empty;
}

// ============= ADMIN SERVICE =============
public interface IAdminService
{
    Task<DashboardDto> GetDashboardAsync();
    Task<IEnumerable<ReportDto>> GetSalesReportsAsync();
}

public class AdminService : IAdminService
{
    private readonly TimeXDbContext _context;

    public AdminService(TimeXDbContext context) => _context = context;

    public async Task<DashboardDto> GetDashboardAsync()
    {
        var totalUsers = await _context.Users.CountAsync();
        var totalProducts = await _context.Products.CountAsync(p => p.IsActive);
        var totalOrders = await _context.Orders.CountAsync();
        var totalRevenue = (await _context.Orders.ToListAsync()).Sum(o => o.TotalAmount);

        return new DashboardDto
        {
            TotalUsers = totalUsers,
            TotalProducts = totalProducts,
            TotalOrders = totalOrders,
            TotalRevenue = totalRevenue
        };
    }

    public async Task<IEnumerable<ReportDto>> GetSalesReportsAsync()
    {
        var orders = await _context.Orders
            .GroupBy(o => o.CreatedAt.Date)
            .Select(g => new ReportDto
            {
                Date = g.Key,
                TotalSales = g.Sum(o => o.TotalAmount),
                OrderCount = g.Count()
            })
            .OrderByDescending(r => r.Date)
            .ToListAsync();

        return orders;
    }
}

public class DashboardDto
{
    public int TotalUsers { get; set; }
    public int TotalProducts { get; set; }
    public int TotalOrders { get; set; }
    public decimal TotalRevenue { get; set; }
}

public class ReportDto
{
    public DateTime Date { get; set; }
    public decimal TotalSales { get; set; }
    public int OrderCount { get; set; }
}
