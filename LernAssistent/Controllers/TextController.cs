using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using System.IO;
using LernAssistent.Interfaces;
using Newtonsoft.Json;

namespace LernAssistent.Controllers
{
    public class TextController
    {
        private static readonly HttpClient _httpClient = new HttpClient();

        // Constructor
        public TextController()
        {
            _httpClient.BaseAddress = new Uri("http://localhost:5001"); // Flask microservice URL
        }

        // Method to send PDF data to the Flask microservice and get the extracted text
        public async Task<string> ConvertToText(byte[] pdfData)
        {
            using (var content = new MultipartFormDataContent())
            {
                // Create the file content and add it to the request
                var fileContent = new ByteArrayContent(pdfData);
                fileContent.Headers.ContentType = MediaTypeHeaderValue.Parse("application/pdf");
                content.Add(fileContent, "file", "uploaded.pdf");

                try
                {
                    // Send the request to the Flask microservice
                    var response = await _httpClient.PostAsync("/api/extract", content);

                    // Check if the response is successful
                    if (response.IsSuccessStatusCode)
                    {
                        // Read the response content
                        var responseContent = await response.Content.ReadAsStringAsync();

                        // Deserialize JSON response to extract text
                        var result = JsonConvert.DeserializeObject<Response>(responseContent);
                        return result?.Text;
                    }
                    else
                    {
                        // Handle unsuccessful response
                        var errorContent = await response.Content.ReadAsStringAsync();
                        return $"Error: {errorContent}";
                    }
                }
                catch (Exception ex)
                {
                    return $"Exception: {ex.Message}";
                }
            }
        }

        // Response class to deserialize JSON response
        public class Response
        {
            public string Text { get; set; }
        }
    }
}
