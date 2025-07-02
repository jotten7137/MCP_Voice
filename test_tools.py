#!/usr/bin/env python3
"""
Test script for MCP Voice tool calling functionality.
"""

import asyncio
import json
import sys
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add the mcp_server to path
sys.path.insert(0, '.')

from mcp_server.core.router import RequestRouter
from mcp_server.tools.calculator import CalculatorTool
from mcp_server.tools.weather import WeatherTool

async def test_tool_extraction():
    """Test tool call extraction from LLM responses."""
    print("\n=== Testing Tool Call Extraction ===")
    
    router = RequestRouter()
    
    # Test various message formats
    test_messages = [
        "I need to calculate 25 * 4. @calculator({\"expression\": \"25 * 4\"})",
        "What's the weather like? @weather({\"location\": \"New York\", \"units\": \"metric\"})",
        "Please calculate 15 + 27 using @calculator({\"expression\": \"15 + 27\"}) and then tell me the result.",
        "I want to know the weather in @weather({\"location\": \"London\"}) please.",
        "Calculate @calculator({\"expression\": \"sqrt(16)\"}) and check weather @weather({\"location\": \"Tokyo\", \"units\": \"metric\"})",
        "Just a regular message with no tool calls",
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\nTest {i}: {message}")
        
        # Simulate LLM response
        llm_response = {
            "message": message,
            "raw_response": message
        }
        
        # Extract tool calls
        tool_calls = router.extract_tool_calls(llm_response)
        
        if tool_calls:
            print(f"  Found {len(tool_calls)} tool call(s):")
            for j, call in enumerate(tool_calls, 1):
                print(f"    {j}. Tool: {call['tool_name']}")
                print(f"       Parameters: {call['parameters']}")
        else:
            print("  No tool calls found")

async def test_tool_execution():
    """Test individual tool execution."""
    print("\n=== Testing Tool Execution ===")
    
    # Test calculator
    print("\nTesting Calculator Tool:")
    calc_tool = CalculatorTool()
    
    test_expressions = [
        "2 + 2",
        "sqrt(16)",
        "10 * 5 + 3",
        "pi * 2",
        "sin(0)",
    ]
    
    for expr in test_expressions:
        try:
            result = await calc_tool.run({"expression": expr})
            print(f"  {expr} = {result}")
        except Exception as e:
            print(f"  {expr} -> Error: {e}")
    
    # Test weather (this will fail without a valid API key, but tests the structure)
    print("\nTesting Weather Tool:")
    weather_tool = WeatherTool()
    
    test_locations = [
        {"location": "New York", "units": "metric"},
        {"location": "London"},
    ]
    
    for params in test_locations:
        try:
            result = await weather_tool.run(params)
            print(f"  {params} -> {result['status']}")
            if result['status'] == 'success':
                formatted = weather_tool.format_for_llm(result)
                print(f"    Formatted: {formatted[:100]}...")
        except Exception as e:
            print(f"  {params} -> Error: {e}")

async def test_full_integration():
    """Test full tool integration workflow."""
    print("\n=== Testing Full Integration ===")
    
    router = RequestRouter()
    router.register_tool("calculator", CalculatorTool())
    router.register_tool("weather", WeatherTool())
    
    # Test messages that should trigger tools
    test_scenarios = [
        {
            "user_message": "What's 15 * 8?",
            "llm_response": "I'll calculate that for you. @calculator({\"expression\": \"15 * 8\"})"
        },
        {
            "user_message": "What's the weather in Paris?",
            "llm_response": "Let me check the weather for you. @weather({\"location\": \"Paris\", \"units\": \"metric\"})"
        },
        {
            "user_message": "Calculate 25 + 17 and tell me the weather in Tokyo",
            "llm_response": "I'll help with both. @calculator({\"expression\": \"25 + 17\"}) @weather({\"location\": \"Tokyo\", \"units\": \"metric\"})"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\nScenario {i}: {scenario['user_message']}")
        print(f"LLM Response: {scenario['llm_response']}")
        
        # Extract tool calls
        tool_calls = router.extract_tool_calls({"message": scenario['llm_response']})
        
        if tool_calls:
            print(f"Extracted {len(tool_calls)} tool call(s)")
            
            # Process tool calls
            results = await router.process_tool_calls(tool_calls)
            
            print("Tool Results:")
            for result in results:
                if result['status'] == 'success':
                    print(f"  ✓ {result['tool_name']}: Success")
                    if 'formatted' in result:
                        print(f"    {result['formatted']}")
                else:
                    print(f"  ✗ {result['tool_name']}: {result.get('error', 'Unknown error')}")
        else:
            print("No tool calls detected")

def test_regex_patterns():
    """Test regex pattern matching."""
    print("\n=== Testing Regex Patterns ===")
    
    test_strings = [
        "@calculator({\"expression\": \"2 + 2\"})",
        "@weather({\"location\": \"New York\"})",
        "@calculator( {\"expression\": \"sqrt(16)\"} )",
        "Text before @calculator({\"expression\": \"5 * 5\"}) text after",
        "@weather({\"location\": \"London\", \"units\": \"metric\"})",
        "Multiple @calculator({\"expression\": \"1 + 1\"}) and @weather({\"location\": \"Tokyo\"})",
        "Malformed @calculator(invalid json)",
        "No tool calls in this message",
    ]
    
    import re
    
    # The pattern from our router
    pattern = r'@(\w+)\s*\(\s*({[^}]*})\s*\)'
    
    for test_str in test_strings:
        print(f"\nTest: {test_str}")
        matches = re.findall(pattern, test_str, re.DOTALL)
        
        if matches:
            for tool_name, params_str in matches:
                print(f"  Found: {tool_name} -> {params_str}")
                try:
                    params = json.loads(params_str.strip())
                    print(f"  Parsed: {params}")
                except json.JSONDecodeError as e:
                    print(f"  JSON Error: {e}")
        else:
            print("  No matches found")

async def main():
    """Run all tests."""
    print("MCP Voice Tool Calling Tests")
    print("=" * 50)
    
    # Run tests
    test_regex_patterns()
    await test_tool_extraction()
    await test_tool_execution()
    await test_full_integration()
    
    print("\n" + "=" * 50)
    print("Tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
