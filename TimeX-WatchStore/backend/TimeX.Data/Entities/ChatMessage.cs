namespace TimeX.Data.Entities;

/// <summary>
/// Represents a chat message for the AI chatbot
/// </summary>
public class ChatMessage
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid UserId { get; set; }
    public User? User { get; set; }
    public string UserMessage { get; set; } = string.Empty;
    public string BotResponse { get; set; } = string.Empty;
    public ChatMessageType MessageType { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}

public enum ChatMessageType
{
    General = 0,
    ProductRecommendation = 1,
    Comparison = 2,
    OccasionBased = 3,
    Specification = 4,
    OrderTracking = 5,
    FAQ = 6,
    Support = 7
}
