 // implement the SendPdf method that retrieves the user information, determines the appropriate AI service to use, and processes the PDF.

using System;
using System.Threading.Tasks;
using LernAssistent.Services.Database;
using LernAssistent.Controllers;

namespace LernAssistent.Controllers
{
    public class MainController
    {   
        private readonly APIController _apiController;
        private readonly AIController _aiController;
        private readonly DatabaseContext _databaseContext;


        public MainController(APIController apiController, AIController aiController, DatabaseContext databaseContext)
        {
            _apiController = apiController;
            _aiController = aiController;
            _databaseContext = databaseContext;
        }


        var textController = new TextController();
        byte[] pdfData = File.ReadAllBytes("/Users/taha/Desktop/001_Taha/002_Studium/002_Uni/001_Fank_UAS/Uni/5.Semester/NachSchreib/Dist_Sys/Lectures/07_blockchains.pdf ");
        string extractedText = await textController.ConvertToText(pdfData);
        Console.WriteLine(extractedText);

    }      
}