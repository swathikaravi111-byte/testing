using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using TimeX.Business.Services;
using System.Security.Claims;

namespace TimeX.API.Controllers;

/// <summary>
/// Product review endpoints
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class ReviewsController : ControllerBase
{
    private readonly IReviewService _reviewService;

    public ReviewsController(IReviewService reviewService) => _reviewService = reviewService;

    private Guid GetUserId()
    {
        var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        return Guid.TryParse(userId, out var guid) ? guid : Guid.Empty;
    }

    /// <summary>
    /// Get reviews for a product
    /// </summary>
    [HttpGet("product/{productId}")]
    public async Task<IActionResult> GetProductReviews(Guid productId)
    {
        try
        {
            var reviews = await _reviewService.GetProductReviewsAsync(productId);
            return Ok(reviews);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { message = ex.Message });
        }
    }

    /// <summary>
    /// Create review (Authorized)
    /// </summary>
    [HttpPost]
    [Authorize]
    public async Task<IActionResult> CreateReview([FromBody] CreateReviewDto dto)
    {
        try
        {
            var userId = GetUserId();
            dto.UserId = userId;
            var review = await _reviewService.CreateReviewAsync(dto);
            return CreatedAtAction(nameof(GetProductReviews), new { productId = dto.ProductId }, review);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { message = ex.Message });
        }
    }

    /// <summary>
    /// Update review (Authorized)
    /// </summary>
    [HttpPut("{id}")]
    [Authorize]
    public async Task<IActionResult> UpdateReview(Guid id, [FromBody] UpdateReviewDto dto)
    {
        try
        {
            var review = await _reviewService.UpdateReviewAsync(id, dto);
            return Ok(review);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { message = ex.Message });
        }
    }

    /// <summary>
    /// Delete review (Authorized)
    /// </summary>
    [HttpDelete("{id}")]
    [Authorize]
    public async Task<IActionResult> DeleteReview(Guid id)
    {
        try
        {
            var result = await _reviewService.DeleteReviewAsync(id);
            return result ? Ok(new { message = "Review deleted" }) : NotFound();
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { message = ex.Message });
        }
    }
}
