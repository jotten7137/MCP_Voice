# MCP Voice Tool Calling Test Guide

## Overview
This guide helps you test the tool calling functionality in MCP Voice after implementing the fixes.

## Quick Setup
1. Run the startup check: `python startup_check.py`
2. Start the server: `python -m mcp_server.main`
3. Open the web interface: `http://localhost:8000`

## Available Tools

### Calculator Tool
- **Purpose**: Perform mathematical calculations
- **Format**: `@calculator({"expression": "mathematical expression"})`
- **Examples**:
  - `@calculator({"expression": "2 + 2"})`
  - `@calculator({"expression": "sqrt(16)"})`
  - `@calculator({"expression": "pi * 2"})`

### Weather Tool  
- **Purpose**: Get weather information for locations
- **Format**: `@weather({"location": "city name", "units": "metric|imperial"})`
- **Examples**:
  - `@weather({"location": "New York"})`
  - `@weather({"location": "London", "units": "metric"})`
  - `@weather({"location": "Tokyo", "units": "imperial"})`

## Test Messages for Users

### Simple Calculator Tests
Try these messages and see if the LLM responds with tool calls:

1. "What is 25 times 4?"
2. "Calculate the square root of 64"
3. "What's 15 + 27?"
4. "Can you compute 2 to the power of 8?"
5. "What's the value of pi times 3?"

### Weather Tests
1. "What's the weather in New York?"
2. "How's the weather in London today?"
3. "Check the weather in Tokyo"
4. "What's the temperature in Paris in Celsius?"

### Combined Tests
1. "Calculate 20 + 15 and tell me the weather in San Francisco"
2. "What's 5 times 7, and how's the weather in Boston?"

## Expected Behavior

### When Tool Calling Works:
1. **User Input**: "What is 25 times 4?"
2. **LLM Response**: "I'll calculate that for you. @calculator({"expression": "25 * 4"})"
3. **System**: Detects tool call, executes calculator
4. **Tool Result**: `{"expression": "25 * 4", "result": 100, "formatted": "100"}`
5. **Final Response**: "The result of 25 × 4 is 100."

### When Tool Calling Fails:
- LLM responds normally without using tool syntax
- Tool calls aren't detected in the response
- Tools fail to execute due to parameter errors

## Troubleshooting

### If Tools Aren't Being Called:
1. Check server logs for tool extraction messages
2. Verify the LLM is including `@tool_name({...})` syntax
3. Make sure the prompt includes tool instructions

### If Tool Calls Fail:
1. Check parameter format (must be valid JSON)
2. Verify tool names match registered tools
3. Check for required parameters

### Common Issues:

#### 1. LLM Not Using Tool Format
**Problem**: LLM responds naturally without tool calls
**Solution**: The prompt needs to be more explicit about tool usage

#### 2. JSON Parsing Errors
**Problem**: `Failed to parse tool call parameters`
**Solution**: Check that parameters are valid JSON with proper quotes

#### 3. Tool Not Found
**Problem**: `Tool 'xyz' not found`
**Solution**: Verify tool is registered in main.py

#### 4. Weather API Errors
**Problem**: Weather tool fails with API errors
**Solution**: Check WEATHER_API_KEY in .env file

## Debug Commands

### Check Tool Registration:
```bash
python debug_tools.py
```

### View Server Logs:
Look for these log messages:
- `Tool registered: calculator`
- `Tool registered: weather`
- `Extracting tool calls from message`
- `Successfully extracted tool call`
- `Processing X tool calls`

### Test Individual Components:
```python
# Test calculator directly
from mcp_server.tools.calculator import CalculatorTool
tool = CalculatorTool()
result = await tool.run({"expression": "2 + 2"})
print(result)
```

## Example Conversation Flow

```
User: What's 15 times 8?

LLM: I'll calculate that for you. @calculator({"expression": "15 * 8"})

System Log:
- Extracting tool calls from message: I'll calculate that for you. @calculator({"expression": "15 * 8"})
- Successfully extracted tool call: calculator with params {'expression': '15 * 8'}
- Processing 1 tool calls
- Executing tool: calculator with params: {'expression': '15 * 8'}
- Tool execution results: [{'status': 'success', 'tool_name': 'calculator', 'result': {...}}]

Final Response: The calculation 15 × 8 equals 120.
```

## Key Files Modified

1. **`mcp_server/models/ollama_llm.py`**: Updated prompt to include tool instructions
2. **`mcp_server/core/router.py`**: Improved tool call extraction with better regex
3. **`mcp_server/main.py`**: Enhanced tool call processing workflow
4. **`app.js`**: Added frontend debugging for tool calls

## Testing Checklist

- [ ] Server starts without errors
- [ ] Tools are registered correctly
- [ ] Calculator tool works with simple expressions
- [ ] Weather tool connects to API (with valid key)
- [ ] Tool calls are extracted from LLM responses
- [ ] Tool results are processed and returned
- [ ] Frontend displays tool call information
- [ ] Audio responses work with tool results

## Next Steps

If tool calling is working:
1. Test with more complex expressions
2. Add additional tools as needed
3. Improve error handling
4. Add tool call history/logging

If still having issues:
1. Check the server logs carefully
2. Run the debug scripts
3. Verify Ollama model responses include tool syntax
4. Consider trying different prompting strategies
