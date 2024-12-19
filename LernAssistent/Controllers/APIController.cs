using System;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;


namespace LernAssistent.Controllers
{
    public class APIController
    {

        
        public async Task<IActionResult> UploadPdf(byte[] pdfData, int UserId)
        {
            // Validate the request
            // ...

            // Forward the request to the MainController
            var result = await _mainController.SendPdf(pdfData);

            // Return the appropriate response
            return Ok(result);
        }
    }
}