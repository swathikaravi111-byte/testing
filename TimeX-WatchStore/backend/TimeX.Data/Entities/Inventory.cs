namespace TimeX.Data.Entities;

/// <summary>
/// Represents inventory/stock for products
/// </summary>
public class Inventory
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid ProductId { get; set; }
    public Product? Product { get; set; }
    public int Quantity { get; set; }
    public int ReservedQuantity { get; set; }
    public int MinimumStockLevel { get; set; }
    public string? WarehouseLocation { get; set; }
    public DateTime LastRestockedAt { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

    public int AvailableQuantity => Quantity - ReservedQuantity;
}
