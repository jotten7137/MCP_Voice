#!/usr/bin/env python3
"""
Startup script for MCP Voice with tool calling enabled.
"""

import sys
import os
import subprocess
import time

def check_requirements():
    """Check if all required packages are installed."""
    print("Checking requirements...")
    
    # Essential packages for basic functionality
    essential_packages = {
        'fastapi': 'FastAPI web framework',
        'uvicorn': 'ASGI server',
        'aiohttp': 'HTTP client library',
        'gtts': 'Google Text-to-Speech',
        'python-multipart': 'Form data parsing'
    }
    
    # Optional packages for enhanced functionality
    optional_packages = {
        'pydantic': 'Data validation',
        'numpy': 'Numerical computing',
        'sympy': 'Symbolic mathematics',
        'python-dotenv': 'Environment configuration'
    }
    
    missing_essential = []
    missing_optional = []
    
    # Check essential packages
    for package, description in essential_packages.items():
        try:
            # Handle special cases
            if package == 'python-multipart':
                import multipart
            elif package == 'python-dotenv':
                import dotenv
            else:
                __import__(package)
        except ImportError:
            missing_essential.append((package, description))
    
    # Check optional packages
    for package, description in optional_packages.items():
        try:
            if package == 'python-dotenv':
                import dotenv
            else:
                __import__(package)
        except ImportError:
            missing_optional.append((package, description))
    
    if missing_essential:
        print(f"❌ Missing essential packages:")
        for package, desc in missing_essential:
            print(f"  - {package}: {desc}")
        print("\n📦 Quick install command:")
        package_names = [pkg for pkg, _ in missing_essential]
        print(f"pip install {' '.join(package_names)}")
        print("\n📋 Or install from requirements file:")
        print("pip install -r requirements-minimal.txt")
        return False
    
    print("✅ All essential packages are installed")
    
    if missing_optional:
        print(f"⚠️  Optional packages missing (recommended):")
        for package, desc in missing_optional:
            print(f"  - {package}: {desc}")
        print("\n📦 Install optional packages:")
        package_names = [pkg for pkg, _ in missing_optional]
        print(f"pip install {' '.join(package_names)}")
    
    return True

def check_config():
    """Check configuration."""
    print("\nChecking configuration...")
    
    # Check if .env file exists
    env_path = ".env"
    if os.path.exists(env_path):
        print("✅ .env file found")
        
        # Read and display key configs
        with open(env_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    print(f"  {line.strip()}")
    else:
        print("⚠️  .env file not found - using defaults")
    
    return True

def test_tools():
    """Test tool functionality."""
    print("\nTesting tools...")
    
    try:
        # Run our debug script
        result = subprocess.run([sys.executable, 'debug_tools.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Tool testing passed")
            # Show key parts of output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Test' in line or '✓' in line or '✗' in line:
                    print(f"  {line}")
        else:
            print("❌ Tool testing failed")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Tool testing timed out")
        return False
    except Exception as e:
        print(f"❌ Tool testing error: {e}")
        return False
    
    return True

def check_ollama():
    """Check if Ollama is running."""
    print("\nChecking Ollama connection...")
    
    try:
        import aiohttp
        import asyncio
        
        async def check_ollama_async():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://localhost:11434/api/tags', timeout=5) as response:
                        if response.status == 200:
                            data = await response.json()
                            models = [model['name'] for model in data.get('models', [])]
                            print(f"✅ Ollama is running with models: {models}")
                            
                            # Check if our default model is available
                            default_model = "llama3.2:latest"
                            if any(default_model in model for model in models):
                                print(f"✅ Default model {default_model} is available")
                            else:
                                print(f"⚠️  Default model {default_model} not found")
                                print(f"Available models: {models}")
                            
                            return True
                        else:
                            print(f"❌ Ollama responded with status {response.status}")
                            return False
            except Exception as e:
                print(f"❌ Cannot connect to Ollama: {e}")
                print("Make sure Ollama is running and accessible at http://localhost:11434")
                return False
        
        return asyncio.run(check_ollama_async())
        
    except ImportError:
        print("❌ aiohttp not installed")
        return False

def main():
    """Main startup sequence."""
    print("MCP Voice Startup Check")
    print("=" * 50)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    checks = [
        ("Requirements", check_requirements),
        ("Configuration", check_config), 
        ("Tools", test_tools),
        ("Ollama", check_ollama),
    ]
    
    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 All checks passed! Ready to start MCP Voice")
        print("\nTo start the server:")
        print("  python -m mcp_server.main")
        print("\nOr use uvicorn directly:")
        print("  uvicorn mcp_server.main:app --host 0.0.0.0 --port 8000 --reload")
        print("\nThen open: http://localhost:8000")
        print("\nTry these test messages:")
        print("  - 'What is 15 times 8?'")
        print("  - 'Calculate the square root of 144'")
        print("  - 'What's the weather in London?'")
    else:
        print("❌ Some checks failed. Please fix the issues above before starting.")
    
    return all_passed

if __name__ == "__main__":
    main()
