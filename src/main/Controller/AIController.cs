using Microsoft.AspNetCore.Mvc;
using Lernassistent.src.main.services;  // For IAIService
using Lernassistent.src.main.Models;
using System.Threading.Tasks;

namespace Lernassistent.src.main.Controller
{
    [ApiController] // Automatically validates incoming requests and provides model validation error responses.
    [Route("api/[controller]")]
    public class AIController : ControllerBase
    {
        private readonly IAIService _aiService;

        // Inject IAIService into the controller
        public AIController(IAIService aiService)
        {
            _aiService = aiService;
        }

        [HttpPost("process")] // Defines a POST endpoint accessible at api/ai/process.

        public async Task<IActionResult> ProcessRequest([FromBody] AIRequest request)
        {
            // Delegate the logic to AIService for processing
            var aiResponse = await _aiService.ProcessRequest(request);

            if (!aiResponse.Success)
            {
                // Return a bad request if AI processing fails
                return BadRequest(aiResponse.Message);
            }

            // Return OK with AI response
            return Ok(new 
            { 
                extractedText = aiResponse.ExtractedText,
                aiResult = aiResponse.AiResult 
            });
        }
    }

    public class AIRequest
    {
        public string? UserId { get; set; }  // Adjusted UserId type to string
        public string? PdfBase64 { get; set; }  // PdfBase64 is required
    }
}
