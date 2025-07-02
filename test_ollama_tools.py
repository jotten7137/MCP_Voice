#!/usr/bin/env python3
"""
Direct test of the Ollama LLM with tool calling
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_ollama_tool_calling():
    """Test Ollama tool calling directly"""
    print("Testing Ollama Tool Calling")
    print("=" * 40)
    
    try:
        from mcp_server.models.ollama_llm import OllamaLLMService
        from mcp_server.core.router import RequestRouter
        
        # Initialize services
        llm = OllamaLLMService()
        router = RequestRouter()
        
        # Test questions that should trigger tool calls
        test_questions = [
            "What's the weather in London?",
            "What is 25 + 17?",
            "Can you calculate 5 * 8?",
            "How's the weather in New York?",
            "What's the square root of 64?"
        ]
        
        for question in test_questions:
            print(f"\nQuestion: {question}")
            
            # Get LLM response
            response = await llm.generate_response(question)
            llm_text = response.get("message", "")
            
            print(f"LLM Response: {llm_text}")
            
            # Check for tool calls
            tool_calls = router.extract_tool_calls({"message": llm_text})
            
            if tool_calls:
                print(f"✓ Found {len(tool_calls)} tool call(s):")
                for call in tool_calls:
                    print(f"  - {call['tool_name']}: {call['parameters']}")
            else:
                print("✗ No tool calls detected")
                
        print("\n" + "=" * 40)
        print("Test completed")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ollama_tool_calling())
