from Services.AIExternalService import AIExternalService
from Services.AILocalService import AILocalService
from Services.AITextProcessor import AITextProcessor
from Services.TextExtractor import TextExtractor

class SummaryProcessor:
    def __init__(self, api_key, external_api_url, local_api_url, text_extractor_url):
        # Create instances for both external and local services
        self.ai_external_service = AIExternalService(api_key, external_api_url)
        self.ai_local_service = AILocalService(local_api_url)
        self.text_extractor = TextExtractor(text_extractor_url)

    async def get_summary(self, pdf_data, use_local=False, title=None):
        """
        Generates a summary of the provided PDF data.
        Optionally includes the title if provided.
        """
        # Extract text from the PDF data
        extracted_text = self.text_extractor.convert_to_text(pdf_data)
        if "Error" in extracted_text or "Exception" in extracted_text:
            return {"error": extracted_text}

        # Instruction to summarize the content 
        instruction = "give me a summary of the following content :"

        # Add title to instruction if provided
        if title:
            instruction = f"Summarize the content titled '{title}' and then: {instruction}"

        # Choose the appropriate AI service (local or external)
        ai_service = self.ai_local_service if use_local else self.ai_external_service

        # Use AITextProcessor to process the text with the chosen service
        ai_text_processor = AITextProcessor(ai_service)
        summary = await ai_text_processor.process_text(extracted_text, user_id=None, use_local=use_local, instruction=instruction)

        summary_response = {
            "status": "success",
            "data": {
                "summary": summary,
                "details": {
                    "length": len(summary),
                    "generated_with": "external_ai" if not use_local else "local_ai",
                }
            }
        }
        return summary_response

