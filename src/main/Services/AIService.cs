using Lernassistent.src.main.database;
using Microsoft.AspNetCore.Mvc;
using System.Linq;
using System.Threading.Tasks;
using Lernassistent.src.main.Models;
using Microsoft.Extensions.Configuration;
using Lernassistent.src.main.services;

namespace Lernassistent.src.main.services
{
    public class AIService
    {
        private readonly DatabaseContext _dbContext;
        private readonly PdfService _pdfService;
        private readonly AIExternalService _aiExternalService;
        private readonly AILocalService _aILocalService;

        public AIService(DatabaseContext dbContext, PdfService pdfService, AIExternalService aiExternalService, AILocalService aILocalService)
        {
            _dbContext = dbContext;
            _pdfService = pdfService;
            _aiExternalService = aiExternalService;
            _aILocalServiceIService = aILocalService;
        }

        public async Task<IActionResult> ProcessRequest(AIRequest request)
        {
            if (request.UserId == null)
            {
                return new BadRequestObjectResult("UserId is required.");
            }

            string userIdAsString = request.UserId?.ToString();

            if (string.IsNullOrEmpty(userIdAsString))
            {
                return new BadRequestObjectResult("Invalid UserId.");
            }

            var user = _dbContext.Users.FirstOrDefault(u => u.UserId == userIdAsString);

            if (user == null)
            {
                return new BadRequestObjectResult("User not found.");
            }

            // Step 1: Extract Text from PDF (if provided)
            string extractedText = string.Empty;
            if (!string.IsNullOrEmpty(request.PdfBase64))
            {
                extractedText = await _pdfService.ExtractTextFromPdfAsync(request.PdfBase64);
            }

            // Step 2: Decide which AI to use based on user's credits
            if (user.Credits > 0)
            {
                // Deduct credits and save to the database
                user.Credits--;
                _dbContext.SaveChanges();

                // Route to external AI
                return await _aiExternalService.CallExternalAI(request, extractedText);
            }
            else
            {
                // Route to local AI
                return LocalAI(request, extractedText);
            }
        }

        private IActionResult LocalAI(AIRequest request, string extractedText)
        {
            // Call the local AI service or process the request locally
            var result = _aILocalService.ProcessLocally(extractedText);
            return new OkObjectResult(result);
        }
    }
}
