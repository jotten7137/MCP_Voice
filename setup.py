#!/usr/bin/env python3
"""
Quick setup script for MCP Voice
Installs required packages and verifies installation
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")
        return False

def install_requirements_file(file_path):
    """Install packages from requirements file."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install from {file_path}: {e}")
        return False

def main():
    """Main installation process."""
    print("MCP Voice Setup Script")
    print("=" * 40)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Installing essential packages...")
    
    # Try requirements file first
    if os.path.exists("requirements-minimal.txt"):
        print("📋 Installing from requirements-minimal.txt...")
        if install_requirements_file("requirements-minimal.txt"):
            print("✅ Successfully installed from requirements file")
        else:
            print("❌ Requirements file installation failed, trying individual packages...")
            
            # Fallback to individual packages
            essential_packages = [
                "fastapi>=0.104.0",
                "uvicorn[standard]>=0.24.0", 
                "aiohttp>=3.9.0",
                "gtts>=2.4.0",
                "python-multipart>=0.0.6",
                "python-dotenv>=1.0.0"
            ]
            
            failed = []
            for package in essential_packages:
                print(f"Installing {package}...")
                if not install_package(package):
                    failed.append(package)
            
            if failed:
                print(f"❌ Failed to install: {', '.join(failed)}")
                return False
    else:
        print("📦 requirements-minimal.txt not found, installing individual packages...")
        
        essential_packages = [
            "fastapi",
            "uvicorn[standard]", 
            "aiohttp",
            "gtts",
            "python-multipart",
            "python-dotenv"
        ]
        
        failed = []
        for package in essential_packages:
            print(f"Installing {package}...")
            if not install_package(package):
                failed.append(package)
        
        if failed:
            print(f"❌ Failed to install: {', '.join(failed)}")
            return False
    
    print("\n🔍 Verifying installation...")
    
    # Run startup check
    try:
        result = subprocess.run([sys.executable, "startup_check.py"], 
                              capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("\n🎉 Setup completed successfully!")
            print("\nNext steps:")
            print("1. Start the server: python -m mcp_server.main")
            print("2. Open browser: http://localhost:8000")
            print("3. Test tool calling with math or weather questions")
            return True
        else:
            print("\n⚠️  Setup completed with warnings. Check the output above.")
            return True
            
    except Exception as e:
        print(f"Could not run verification: {e}")
        print("Manual check: python startup_check.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check error messages above.")
        sys.exit(1)
    else:
        print("\n✅ Setup complete!")
