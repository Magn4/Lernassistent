namespace Lernassistent.src.main.controller
{
    using Microsoft.AspNetCore.Mvc;
    using System.Net.Http;
    using System.Text;
    using System.Threading.Tasks;
    using Microsoft.Data.Sqlite; // For SQLite usage
    using Microsoft.Extensions.Configuration; // For configuration
    using System;

    [ApiController]
    [Route("api/[controller]")]
    public class ApiController : ControllerBase
    {
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly IConfiguration _configuration; // Added for fetching API keys
        private readonly string _connectionString = "Data Source=credits.db";
        private readonly string _externalAIBaseUrl;

        public ApiController(IHttpClientFactory httpClientFactory, IConfiguration configuration)
        {
            _httpClientFactory = httpClientFactory;
            _configuration = configuration; // Initialize the configuration
            _externalAIBaseUrl = _configuration["ExternalAI:BaseUrl"]; // Fetch external AI service base URL from configuration
            InitializeDatabase();
        }

        // Initialize the database
        private void InitializeDatabase()
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText = @"
                    CREATE TABLE IF NOT EXISTS Users (
                        UserId TEXT PRIMARY KEY,
                        Credits INT DEFAULT 100
                    );
                ";
                command.ExecuteNonQuery();
            }
        }

        [HttpPost("process-pdf")]
        public async Task<IActionResult> ProcessPdf([FromBody] PdfRequest pdfRequest)
        {
            if (pdfRequest?.UserId == null || pdfRequest?.PdfBase64 == null)
            {
                return BadRequest("UserId and PdfBase64 are required.");
            }

            var httpClient = _httpClientFactory.CreateClient();

            // Step 1: Send PDF to Text Extractor Service
            var textResponse = await httpClient.PostAsync("http://text-extractor-service/api/extract",
                new StringContent(pdfRequest.PdfBase64, Encoding.UTF8, "application/json"));

            if (!textResponse.IsSuccessStatusCode) return BadRequest("Failed to extract text");

            var extractedText = await textResponse.Content.ReadAsStringAsync();

            // Step 2: Decide whether to use Local or External AI
            var userCredits = GetUserCredits(pdfRequest.UserId);
            var useLocalAI = userCredits <= 0;

            // Step 3: Send to appropriate AI Service

            // External AI Service uses Bearer Token
            var aiServiceUrl = useLocalAI ? "http://ai-service/api/ai" : $"{_externalAIBaseUrl}/api/ai";
            var aiPayload = new StringContent(
                $"{{ \"text\": \"{extractedText}\", \"use_local\": {useLocalAI.ToString().ToLower()} }}",
                Encoding.UTF8,
                "application/json"
            );

            // Adding Bearer Token to Authorization header for External AI Service
            if (!useLocalAI)
            {
                var apiKey = _configuration["ExternalAI:ApiKey"]; // Fetch the API Key from configuration
                httpClient.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", apiKey);
            }

            var aiResponse = await httpClient.PostAsync(aiServiceUrl, aiPayload);

            if (!aiResponse.IsSuccessStatusCode) return BadRequest("AI processing failed");

            var aiResult = await aiResponse.Content.ReadAsStringAsync();

            // Step 4: Deduct credits for external AI usage
            if (!useLocalAI) DeductCredits(pdfRequest.UserId);

            return Ok(new { extractedText, aiResult });
        }

        // Get user credits from the database
        private int GetUserCredits(string userId)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText = "SELECT Credits FROM Users WHERE UserId = @userId";
                command.Parameters.AddWithValue("@userId", userId);

                var result = command.ExecuteScalar();
                return result != null ? Convert.ToInt32(result) : InitializeUserCredits(userId);
            }
        }

        // Initialize credits for a new user
        private int InitializeUserCredits(string userId)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText = "INSERT INTO Users (UserId, Credits) VALUES (@userId, 100)";
                command.Parameters.AddWithValue("@userId", userId);
                command.ExecuteNonQuery();
            }
            return 100;
        }

        // Deduct credits from the user
        private void DeductCredits(string userId)
        {
            using (var connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                var command = connection.CreateCommand();
                command.CommandText = "UPDATE Users SET Credits = Credits - 1 WHERE UserId = @userId";
                command.Parameters.AddWithValue("@userId", userId);
                command.ExecuteNonQuery();
            }
        }
    }

    public class PdfRequest
    {
        public string? UserId { get; set; } // User-specific ID
        public string? PdfBase64 { get; set; }
    }
}
