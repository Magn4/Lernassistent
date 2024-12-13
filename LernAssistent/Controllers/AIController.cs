using System;
using System.Threading.Tasks;


public class AIController
{
    public readonly AiExternalService AiExternalService;
    public readonly AiInternalService AiInternalService;

    public AIController(AiExternalService aiExternalService, AiInternalService aiInternalService)
    {
        AiExternalService = aiExternalService;
        AiInternalService = aiInternalService;
    }
}
