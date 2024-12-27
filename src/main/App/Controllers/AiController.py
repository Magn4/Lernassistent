class AIController:
    def __init__(self, external_service, local_service):
        self.external_service = external_service
        self.local_service = local_service

    async def process_text(self, text, use_local):
        """
        Process the text using either the external or local LLM service based on the flag.
        """
        if use_local:
            return await self.local_service.process_text(text)
        else:
            return await self.external_service.process_text(text)