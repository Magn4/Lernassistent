# InstructionProcessor.py 

# InstructionProcessor.py

from Services.AIExternalService import AIExternalService

from Services.AILocalService import AILocalService
from Services.AITextProcessor import AITextProcessor

class InstructionProcessor:
    def __init__(self, api_key, external_api_url, local_api_url):
        # Create instances for both external and local services
        self.ai_external_service = AIExternalService(api_key, external_api_url)
        self.ai_local_service = AILocalService(local_api_url)

    async def get_summary(self, text, use_local=False):
        """
        Generates a summary of the provided text.
        """
        # Instruction to summarize the content in 2 sentences
        instruction = "give me a summary of the following content in 2 sentences:"
        
        # Choose the appropriate AI service (local or external)
        ai_service = self.ai_local_service if use_local else self.ai_external_service
        
        # Use AITextProcessor to process the text with the chosen service
        ai_text_processor = AITextProcessor(ai_service)
        return await ai_text_processor.process_text(text, user_id=None, use_local=use_local, instruction=instruction)

    async def get_explanation(self, text, use_local=False):
        """
        Generates a detailed explanation of the provided text.
        """
        # Instruction to explain the content in detail
        instruction = "explain the following content in detail:"
        
        # Choose the appropriate AI service (local or external)
        ai_service = self.ai_local_service if use_local else self.ai_external_service
        
        # Use AITextProcessor to process the text with the chosen service
        ai_text_processor = AITextProcessor(ai_service)
        return await ai_text_processor.process_text(text, user_id=None, use_local=use_local, instruction=instruction)
