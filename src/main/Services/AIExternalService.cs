using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.AspNetCore.Mvc;

using Lernassistent.src.main.Controller;

namespace Lernassistent.src.main.services
{
    public class AIExternalService
    {
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly IConfiguration _configuration;

        public AIExternalService(IHttpClientFactory httpClientFactory, IConfiguration configuration)
        {
            _httpClientFactory = httpClientFactory;
            _configuration = configuration;
        }

        public async Task<IActionResult> CallExternalAI(AIRequest request, string extractedText)
        {
            try
            {
                var httpClient = _httpClientFactory.CreateClient();
                var apiKey = _configuration["ExternalAI:ApiKey"];
                httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);

                var aiRequest = new
                {
                    text = extractedText,
                    userId = request.UserId
                };
                var payload = new StringContent(JsonSerializer.Serialize(aiRequest), Encoding.UTF8, "application/json");

                var response = await httpClient.PostAsync($"{_configuration["ExternalAI:BaseUrl"]}/api/ai", payload);

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    return new OkObjectResult(new { Message = "Request routed to external AI", Result = responseContent });
                }

                return new BadRequestObjectResult("External AI request failed");
            }
            catch (Exception ex)
            {
                return new ObjectResult($"External AI call error: {ex.Message}") { StatusCode = 500 };
            }
        }
    }
}
