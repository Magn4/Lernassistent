namespace Lernassistent.src.main.Models
{
    // Response class for AI processing results
    public class AIResponse
    {
        public bool Success { get; set; }
        public string Message { get; set; }  // Message to explain success or failure
        public string? ExtractedText { get; set; }  // Text extracted from PDF, if applicable
        public string? AiResult { get; set; }  // The AI result, if processed successfully
    }
}
