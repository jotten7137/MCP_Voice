#!/usr/bin/env python3
"""
Simple test to verify Ollama tool calling with different models
"""

import asyncio
import aiohttp
import json

async def test_ollama_direct():
    """Test Ollama API directly with tool calling instructions"""
    
    models_to_test = ["qwq:32b", "llama3.2:latest", "deepseek-r1:8b"]
    
    system_message = """You are an AI assistant with tool access.

For weather questions: respond with @weather({"location": "CITY"})
For math questions: respond with @calculator({"expression": "MATH"})

No explanations needed, just the tool call."""
    
    test_questions = [
        "What's the weather in London?",
        "What is 25 + 17?",
    ]
    
    for model in models_to_test:
        print(f"\n=== Testing {model} ===")
        
        for question in test_questions:
            print(f"\nQuestion: {question}")
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": model,
                            "prompt": f"User: {question}\n\nAssistant:",
                            "system": system_message,
                            "stream": False,
                            "options": {
                                "temperature": 0.1,
                                "max_tokens": 100
                            }
                        }
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            response_text = data.get("response", "")
                            print(f"Response: {response_text}")
                            
                            # Check for tool calls
                            if "@weather(" in response_text or "@calculator(" in response_text:
                                print("✓ Tool call detected!")
                            else:
                                print("✗ No tool call detected")
                        else:
                            print(f"Error: HTTP {response.status}")
                            
            except Exception as e:
                print(f"Error testing {model}: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama_direct())
