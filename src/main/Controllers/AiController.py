import asyncio

class AIController:
    def __init__(self, ai_external_service, ai_internal_service, database_context):
        # Initialize the external and internal AI services
        self.ai_external_service = ai_external_service
        self.ai_internal_service = ai_internal_service
        self.database_context = database_context

    async def process_text(self, text: str) -> str:
        # Retrieve user information from the database (simulating an async DB call)
        user_info = await self.database_context.get_user_info_async()

        # Determine which AI service to use based on the user's credit balance
        ai_service = self.ai_external_service if user_info['credit_balance'] > 100 else self.ai_internal_service

        # Process the text using the selected AI service
        result = await ai_service.process_text(text)

        return result

# Example usage
async def main():
    # Simulate an external service API URL and API key
    api_url = "https://external-ai-api.com/process"  # Replace with actual API URL
    api_key = "your-api-key-here"
    
    # Initialize services
    external_service = AiExternalService(api_url, api_key)
    internal_service = AiInternalService()
    
    # Mock database context (you should implement the actual context and method)
    class MockDatabaseContext:
        async def get_user_info_async(self):
            # Simulate a database call that returns user data with credit balance
            return {"credit_balance": 150}

    database_context = MockDatabaseContext()
    
    # Initialize the AIController
    ai_controller = AIController(external_service, internal_service, database_context)
    
    # Process some text
    text = "This is some text that needs to be processed."
    result = await ai_controller.process_text(text)
    
    print(result)

# Run the main function asynchronously
if __name__ == "__main__":
    asyncio.run(main())
