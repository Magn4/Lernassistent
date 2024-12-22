class AIController:
    def __init__(self, external_service, internal_service, db_context):
        self.external_service = external_service
        self.internal_service = internal_service
        self.db_context = db_context

    async def process_text(self, text, user_id):
        """
        Use the AIController to process the extracted text based on the user ID.
        """
        user_info = await self.db_context.get_user_info_async(user_id)
        if user_info['credit_balance'] > 100:
            return await self.external_service.process_text(text)
        else:
            return await self.internal_service.process_text(text)
