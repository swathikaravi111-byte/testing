using Xunit;
using Moq;
using TimeX.Business.Services;
using TimeX.Data;
using TimeX.Data.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace TimeX.Tests;

public class AuthServiceTests
{
    private readonly TimeXDbContext _context;
    private readonly IConfiguration _configuration;
    private readonly AuthService _authService;

    public AuthServiceTests()
    {
        var options = new DbContextOptionsBuilder<TimeXDbContext>()
            .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
            .Options;

        _context = new TimeXDbContext(options);

        var configMock = new Mock<IConfiguration>();
        configMock.Setup(x => x.GetSection("JwtSettings")).Returns(new Mock<IConfigurationSection>().Object);
        _configuration = configMock.Object;

        _authService = new AuthService(_context, _configuration);
    }

    [Fact]
    public async Task RegisterAsync_WithValidData_ShouldCreateUser()
    {
        // Arrange
        var request = new RegisterRequest
        {
            Email = "test@example.com",
            Password = "Password@123",
            FirstName = "Test",
            LastName = "User"
        };

        // Act
        var result = await _authService.RegisterAsync(request);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.NotNull(result.User);
        Assert.Equal("test@example.com", result.User.Email);
        Assert.NotNull(result.Token);
    }

    [Fact]
    public async Task RegisterAsync_WithDuplicateEmail_ShouldFail()
    {
        // Arrange
        var email = "duplicate@example.com";
        _context.Users.Add(new User { Email = email, PasswordHash = "hash" });
        await _context.SaveChangesAsync();

        var request = new RegisterRequest
        {
            Email = email,
            Password = "Password@123",
            FirstName = "Test",
            LastName = "User"
        };

        // Act
        var result = await _authService.RegisterAsync(request);

        // Assert
        Assert.False(result.IsSuccess);
        Assert.Contains("already registered", result.Message);
    }

    [Fact]
    public async Task LoginAsync_WithValidCredentials_ShouldReturnToken()
    {
        // Arrange
        var email = "login@example.com";
        var password = "Password@123";
        var user = new User
        {
            Email = email,
            PasswordHash = BCrypt.Net.BCrypt.HashPassword(password),
            FirstName = "Test",
            LastName = "User",
            IsActive = true
        };
        _context.Users.Add(user);
        await _context.SaveChangesAsync();

        var request = new LoginRequest { Email = email, Password = password };

        // Act
        var result = await _authService.LoginAsync(request);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.NotNull(result.Token);
    }

    [Fact]
    public async Task LoginAsync_WithInvalidPassword_ShouldFail()
    {
        // Arrange
        var user = new User
        {
            Email = "test@example.com",
            PasswordHash = BCrypt.Net.BCrypt.HashPassword("CorrectPassword@123"),
            IsActive = true
        };
        _context.Users.Add(user);
        await _context.SaveChangesAsync();

        var request = new LoginRequest { Email = "test@example.com", Password = "WrongPassword" };

        // Act
        var result = await _authService.LoginAsync(request);

        // Assert
        Assert.False(result.IsSuccess);
    }
}
