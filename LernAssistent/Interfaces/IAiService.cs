
namespace LernAssistent.Interfaces
{
    public interface IAiService
    {
        Task<string> ProcessTextAsync(byte[] pdfData);
    }
}