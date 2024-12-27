class AITextProcessor:
    def __init__(self, ai_controller):
        self.ai_controller = ai_controller

    async def process_text(self, text, user_id, use_local, instruction):
        """
        Use the AIController to process the extracted text based on the user ID and selected service.
        """
        full_text = f"{instruction}\n\n{text}"  # Prepend the instruction to the text
        return await self.ai_controller.process_text(full_text, use_local)