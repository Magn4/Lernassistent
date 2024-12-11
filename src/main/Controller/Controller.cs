using Microsoft.AspNetCore.Mvc;
using System.Linq;
using Lernassistent.src.main.database;

namespace Lernassistent.src.main.controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class AIController : ControllerBase
    {
        private readonly DatabaseContext _dbContext;

        public AIController(DatabaseContext dbContext)
        {
            _dbContext = dbContext;
        }

        [HttpPost("process")]
        public IActionResult ProcessRequest([FromBody] AIRequest request)
        {
            // Fetch user from the database
            var user = _dbContext.Users.FirstOrDefault(u => u.Id == request.UserId);

            if (user == null)
            {
                return BadRequest("User not found.");
            }

            // Decide which AI to use based on user's credits
            if (user.Credits > 0)
            {
                // Deduct credits and save to the database
                user.Credits--;
                _dbContext.SaveChanges();

                // Route to external AI
                return ExternalAI(request);
            }
            else
            {
                // Route to local AI
                return LocalAI(request);
            }
        }

        private IActionResult ExternalAI(AIRequest request)
        {
            // Code to call the external AI microservice
            return Ok(new { Message = "Request routed to external AI" });
        }

        private IActionResult LocalAI(AIRequest request)
        {
            // Code to call the local AI microservice
            return Ok(new { Message = "Request routed to local AI" });
        }
    }

    public class AIRequest
    {
        public int UserId { get; set; }
        public string? Query { get; set; }
    }
}
