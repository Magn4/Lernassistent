using System;
using System.Threading.Tasks;
using LernAssistent.Interfaces;
using LernAssistent.Services.AI;

namespace LernAssistent.Controllers
{
    public class AIController
    {
        public readonly AiExternalService AiExternalService;
        public readonly AiInternalService AiInternalService;

        public AIController(AiExternalService aiExternalService, AiInternalService aiInternalService)
        {
            AiExternalService = aiExternalService;
            AiInternalService = aiInternalService;
        }

             public async Task<string> ProcessText(string Text)
        {
            // Retrieve user information from the database
            var userInfo = await _databaseContext.GetUserInfoAsync();

            // Determine which AI service to use based on the user's credit balance
            IAiService aiService = userInfo.CreditBalance > 100 ? _aiController.AiExternalService : _aiController.AiInternalService;

            // Process the PDF using the selected AI service
            var result = await aiService.ProcessTextAsync(Text);

            // Return the result
            return result;
        }
    }
}