from Services.TextExtractor import TextExtractor
from Services.AI.AITextProcessor import AITextProcessor

class TextController:
    def __init__(self, text_extractor, ai_text_processor):
        self.text_extractor = text_extractor
        self.ai_text_processor = ai_text_processor

    def convert_to_text(self, pdf_data):
        return self.text_extractor.convert_to_text(pdf_data)

    async def process_text(self, text, user_id, use_local, instruction):
        return await self.ai_text_processor.process_text(text, user_id, use_local, instruction)