#!/usr/bin/env python3
"""
Simple test to verify tool calling functionality by running the server components directly.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_tool_calling_simple():
    """Test tool calling with minimal setup."""
    print("Testing MCP Voice Tool Calling...")
    print("=" * 50)
    
    try:
        # Import our components
        from mcp_server.core.router import RequestRouter
        from mcp_server.tools.calculator import CalculatorTool
        from mcp_server.tools.weather import WeatherTool
        
        # Create router and register tools
        router = RequestRouter()
        router.register_tool("calculator", CalculatorTool())
        router.register_tool("weather", WeatherTool())
        
        print("✓ Router and tools initialized")
        
        # Test 1: Simple calculator
        print("\nTest 1: Calculator tool directly")
        calc_tool = CalculatorTool()
        result = await calc_tool.run({"expression": "2 + 2"})
        print("Calculator result: {}".format(result))
        
        # Test 2: Tool call extraction
        print("\nTest 2: Tool call extraction")
        test_message = "Please calculate @calculator({\"expression\": \"5 * 5\"}) for me"
        
        llm_response = {
            "message": test_message,
            "raw_response": test_message
        }
        
        tool_calls = router.extract_tool_calls(llm_response)
        print(f"Extracted tool calls: {tool_calls}")
        
        # Test 3: Tool call processing
        if tool_calls:
            print("\nTest 3: Tool call processing")
            results = await router.process_tool_calls(tool_calls)
            print(f"Tool execution results: {results}")
            
            for result in results:
                if result['status'] == 'success':
                    print("Success: {} - {}".format(result['tool_name'], result.get('formatted', 'Success')))
                else:
                    print("Error: {} - {}".format(result['tool_name'], result.get('error', 'Unknown error')))
        
        # Test 4: Multiple tool calls
        print("\nTest 4: Multiple tool calls")
        multi_message = "Calculate @calculator({\"expression\": \"10 + 5\"}) and check weather @weather({\"location\": \"San Francisco\"})"
        
        multi_response = {"message": multi_message}
        multi_calls = router.extract_tool_calls(multi_response)
        print(f"Multiple tool calls extracted: {len(multi_calls)}")
        
        if multi_calls:
            multi_results = await router.process_tool_calls(multi_calls)
            for result in multi_results:
                status = "✓" if result['status'] == 'success' else "✗"
                print(f"{status} {result['tool_name']}: {result.get('formatted', result.get('error', 'No details'))[:100]}")
        
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_tool_calling_simple())
    if success:
        print("\nTool calling appears to be working correctly!")
        print("\nNext steps:")
        print("1. Start the server: python -m mcp_server.main")
        print("2. Open the web interface and try messages like:")
        print("   - 'What is 25 * 4?'")
        print("   - 'Calculate the square root of 64'") 
        print("   - 'What's the weather in New York?'")
        print("\nThe LLM should respond with tool calls that get processed automatically.")
    else:
        print("\nTool calling has issues that need to be resolved.")
