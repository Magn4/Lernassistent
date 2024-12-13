using Microsoft.AspNetCore.Mvc;
using System.Linq;
using System.Threading.Tasks;
using Lernassistent.src.main.database;
using Lernassistent.src.main.services;


namespace Lernassistent.src.main.controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class AIController : ControllerBase
    {
        private readonly DatabaseContext _dbContext;
        private readonly AIExternalService _externalService;
        private readonly AILocalService _localService;

        public AIController(DatabaseContext dbContext, AIExternalService externalService, AILocalService localService)
        {
            _dbContext = dbContext;
            _externalService = externalService;
            _localService = localService;
        }

        [HttpPost("process")]
        public async Task<IActionResult> ProcessRequest([FromBody] AIRequest request)
        {
            // Fetch user from the database
            var user = _dbContext.Users.FirstOrDefault(u => u.Id == request.UserId);

            if (user == null)
            {
                return BadRequest("User not found.");
            }

            // Simulated text extraction for demonstration
            var extractedText = "Sample extracted text for processing";

            if (user.Credits > 0)
            {
                // Deduct credits and save to the database
                user.Credits--;
                await _dbContext.SaveChangesAsync();

                // Route to external AI
                return await _externalService.CallExternalAI(request, extractedText);
            }
            else
            {
                // Route to local AI
                var localResult = _localService.ProcessLocally(extractedText);
                return Ok(new { Message = "Request routed to local AI", Result = localResult });
            }
        }
    }

    public class AIRequest
    {
        public int UserId { get; set; }
        public string? Query { get; set; }
    }
}
