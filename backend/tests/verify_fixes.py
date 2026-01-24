import asyncio
import sys
import os
from unittest.mock import MagicMock, AsyncMock, patch

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Mock settings before importing app modules that might use them
with patch('app.core.config.settings') as mock_settings:
    mock_settings.OPENAI_API_KEY = "sk-test-key"
    mock_settings.AI_MODEL = "gpt-4o-mini"
    mock_settings.REDIS_HOST = "localhost"
    mock_settings.REDIS_PORT = 6379

    from app.api.v1.endpoints.auth import detect_sector, SectorDetectionRequest
    from app.services.ai_service import AIService
    from app.models.tenant import Tenant

async def test_sector_detection_fallback():
    print("\n🧪 Testing Sector Detection Fallback...")
    
    # Mock DB session
    mock_db = AsyncMock()
    
    # Setup mock result for tenant query (return empty to trigger fallback)
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute.return_value = mock_result
    
    # Request causing fallback (unknown domain, no tenant_id)
    request = SectorDetectionRequest(email="unknown@example.com")
    
    response = await detect_sector(request, db=mock_db)
    
    print(f"   Sector: {response.sector}")
    print(f"   Tenant ID: {response.tenant_id}")
    
    # Verification
    if response.tenant_id == "00000000-0000-0000-0000-000000000000":
        print("✅ SUCCESS: Fallback Tenant ID is valid Zero-UUID.")
    else:
        print(f"❌ FAILURE: Fallback Tenant ID is {response.tenant_id}, expected Zero-UUID.")

async def test_ai_caching():
    print("\n🧪 Testing AI Service Caching...")
    
    # Mock OpenAI client
    with patch('app.services.ai_service.get_ai_client') as mock_get_client:
        mock_client = AsyncMock()
        mock_get_client.return_value = mock_client
        
        # Mock API response
        mock_completion = MagicMock()
        mock_completion.choices[0].message.tool_calls[0].function.arguments = '{"intent": "test_intent", "confidence": 0.9}'
        mock_client.chat.completions.create.return_value = mock_completion
        
        # First call (should hit API)
        print("   Calling detect_intent (1st time)...")
        result1 = await AIService.detect_intent("test message")
        
        # Second call (should hit cache)
        print("   Calling detect_intent (2nd time)...")
        result2 = await AIService.detect_intent("test message")
        
        # Verification
        api_call_count = mock_client.chat.completions.create.call_count
        print(f"   API Call Count: {api_call_count}")
        
        if api_call_count == 1:
            print("✅ SUCCESS: Cache worked! API called only once.")
        else:
            print(f"❌ FAILURE: API called {api_call_count} times.")

async def main():
    print("🚀 Starting Analyst Verification...")
    try:
        await test_sector_detection_fallback()
        await test_ai_caching()
    except Exception as e:
        print(f"🔥 CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
