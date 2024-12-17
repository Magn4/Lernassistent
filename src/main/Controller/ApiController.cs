namespace Lernassistent.src.main.controller
{
    using Microsoft.AspNetCore.Mvc; // MVC framework to create API endpoints.
    using System.Threading.Tasks; // Async operations.
    using Lernassistent.src.main.services.interfaces; 
    using Lernassistent.src.main.Models;  // Add the Models namespace here for AIRequest and other models


    [ApiController] // This automatically provides model validation and various API-specific behaviors like response handling.
    [Route("api/[controller]")]
    
    // Important: If you name the controller (e.g., PdfController), the route will be api/pdf.


    public class ApiController : ControllerBase
    {
        private readonly IAIService _aiService;
        private readonly string _connectionString = "Data Source=credits.db";
        
        // Constructor with Dependency Injection
        public ApiController(IAIService aiService)
        {
            _aiService = aiService;
        }

        // Endpoint to process PDF requests
        [HttpPost("process-pdf")]
        public async Task<IActionResult> ProcessPdf([FromBody] PdfRequest pdfRequest) 
        // The [FromBody] attribute binds the request body to the pdfRequest parameter, which is an object containing the user ID and the PDF data in Base64.

        {
            // Validate input
            if (pdfRequest?.UserId == null || pdfRequest?.PdfBase64 == null)
            {
                return BadRequest("UserId and PdfBase64 are required.");
            }

            // Step 1: Process the PDF using AIService
            string aiResult;
            try
            {
                aiResult = await _aiService.ProcessPdfAsync(pdfRequest.UserId, pdfRequest.PdfBase64);
            }
            catch (Exception ex)
            {
                // Return internal server error if something goes wrong
                return StatusCode(500, $"AI processing failed: {ex.Message}");
            }


            // Step 2: Handle AI service results

             if (aiResult.StartsWith("Failed") || aiResult.StartsWith("AI processing failed"))
            {
                return BadRequest(aiResult);  // Return the failure message from AIService
            }

            // If AI processing is successful, return the result
            return Ok(new { extractedText = aiResult, aiResult });
        }
    }

    // Request class to model the incoming PDF request
    public class PdfRequest
    {
        public string? UserId { get; set; }
        public string? PdfBase64 { get; set; }
    }
}
