namespace Lernassistent.src.main.services.interfaces
{
    using System.Threading.Tasks;
    using Lernassistent.src.main.Models;  // Add the Models namespace here for AIRequest, PdfRequest, or Response

    // Interface to handle AI service interactions
    public interface IAIService
    {
        Task<AIResponse> ProcessPdfAsync(PdfRequest request);
    }
}
