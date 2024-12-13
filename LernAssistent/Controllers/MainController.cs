 // implement the SendPdf method that retrieves the user information, determines the appropriate AI service to use, and processes the PDF.

using System;
using System.Threading.Tasks;


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



    // Finish it !!!!
    public async String ConvertToText(byte[] pdfData){}

    public async Task<string> SendText(string Text)
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