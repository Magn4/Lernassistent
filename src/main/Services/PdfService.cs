// PdfService.cs
// Extracts text from PDFs

using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

namespace Lernassistent.src.main.services
{
    public class PdfService
    {
        private readonly IHttpClientFactory _httpClientFactory; // to create HTTP clients for external API calls.
        private readonly IConfiguration _configuration; // to access configuration settings (like the AI base URL and API key).

        public PdfService(IHttpClientFactory httpClientFactory, IConfiguration configuration)
        {
            _httpClientFactory = httpClientFactory;
            _configuration = configuration;
        }

        public async Task<string> ExtractTextFromPdfAsync(string pdfBase64)
        {
            var httpClient = _httpClientFactory.CreateClient();
            var response = await httpClient.PostAsync("http://text-extractor-service/api/extract",
                new StringContent(JsonSerializer.Serialize(new { pdfBase64 }), Encoding.UTF8, "application/json"));

            if (response.IsSuccessStatusCode)
            {
                var extractedText = await response.Content.ReadAsStringAsync();
                return extractedText;
            }

            return "Failed to extract text from PDF.";
        }
    }
}
