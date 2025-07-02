#!/usr/bin/env python3
"""
Quick diagnostic script for MCP Voice tool calling.
Run this to check if tool calling is set up correctly.
"""

import json
import re
import sys
import os

def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if os.path.exists(filepath):
        print(f"✓ {description}: Found")
        return True
    else:
        print(f"✗ {description}: Missing - {filepath}")
        return False

def check_tool_calling_setup():
    """Check if tool calling is properly configured."""
    print("MCP Voice Tool Calling Diagnostic")
    print("=" * 50)
    
    # Check critical files
    files_to_check = [
        ("mcp_server/tools/base.py", "Base tool class"),
        ("mcp_server/tools/calculator.py", "Calculator tool"),
        ("mcp_server/tools/weather.py", "Weather tool"),
        ("mcp_server/core/router.py", "Tool router"),
        ("mcp_server/models/ollama_llm.py", "Ollama LLM service"),
        ("mcp_server/main.py", "Main server"),
    ]
    
    all_good = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_good = False
    
    if not all_good:
        print("\n❌ Some critical files are missing!")
        return False
    
    print("\n📁 All critical files present")
    
    # Check tool registration in main.py
    print("\n🔧 Checking tool registration...")
    try:
        with open("mcp_server/main.py", "r") as f:
            content = f.read()
            
        if "router.register_tool" in content:
            print("✓ Tool registration code found")
        else:
            print("✗ Tool registration code missing")
            all_good = False
            
        if "WeatherTool()" in content and "CalculatorTool()" in content:
            print("✓ Both tools are registered")
        else:
            print("✗ Tool registration incomplete")
            all_good = False
            
    except Exception as e:
        print(f"✗ Error checking main.py: {e}")
        all_good = False
    
    # Check Ollama service configuration
    print("\n🤖 Checking Ollama LLM configuration...")
    try:
        with open("mcp_server/models/ollama_llm.py", "r") as f:
            content = f.read()
            
        if "@tool_name" in content:
            print("✓ Tool calling instructions found in Ollama service")
        else:
            print("✗ Tool calling instructions missing from Ollama service")
            all_good = False
            
    except Exception as e:
        print(f"✗ Error checking ollama_llm.py: {e}")
        all_good = False
    
    # Check router tool extraction
    print("\n🎯 Checking tool extraction logic...")
    try:
        with open("mcp_server/core/router.py", "r") as f:
            content = f.read()
            
        if "extract_tool_calls" in content:
            print("✓ Tool extraction method found")
        else:
            print("✗ Tool extraction method missing")
            all_good = False
            
        if r"@(\w+)" in content:
            print("✓ Tool call regex pattern found")
        else:
            print("✗ Tool call regex pattern missing")
            all_good = False
            
    except Exception as e:
        print(f"✗ Error checking router.py: {e}")
        all_good = False
    
    # Test regex pattern
    print("\n🧪 Testing tool extraction regex...")
    test_message = 'I need to calculate something. @calculator({"expression": "2 + 2"})'
    pattern = r'@(\w+)\s*\(\s*({[^}]*})\s*\)'
    matches = re.findall(pattern, test_message)
    
    if matches:
        print(f"✓ Regex successfully extracted: {matches}")
    else:
        print("✗ Regex failed to extract tool calls")
        all_good = False
    
    # Check configuration
    print("\n⚙️  Checking configuration...")
    try:
        with open("mcp_server/config.py", "r") as f:
            content = f.read()
            
        if "ALLOW_TOOL_CALLS" in content:
            print("✓ Tool calling configuration option found")
        else:
            print("✗ Tool calling configuration option missing")
            all_good = False
            
    except Exception as e:
        print(f"✗ Error checking config.py: {e}")
        all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All checks passed! Tool calling should work.")
        print("\nTo test tool calling:")
        print("1. Start the server: python run.py")
        print("2. Open the web interface")
        print("3. Try: 'What is 15 * 8?'")
        print("4. Try: 'What is the weather in New York?'")
    else:
        print("❌ Some issues found. Please fix the above problems.")
    
    return all_good

def show_example_messages():
    """Show example messages that should trigger tools."""
    print("\n📝 Example messages that should trigger tools:")
    print("-" * 45)
    
    examples = [
        ("Calculator", [
            "What is 15 * 8?",
            "Calculate 25 + 17",
            "What's the square root of 16?",
            "Can you compute 10 * 5 + 3?"
        ]),
        ("Weather", [
            "What's the weather in New York?",
            "Check the weather in London",
            "How's the weather in Tokyo?",
            "What's the temperature in Paris?"
        ])
    ]
    
    for tool_name, messages in examples:
        print(f"\n{tool_name} tool examples:")
        for msg in messages:
            print(f"  • {msg}")

if __name__ == "__main__":
    success = check_tool_calling_setup()
    show_example_messages()
    
    if not success:
        sys.exit(1)
