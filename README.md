PhiData + Ollama AI Agent Setup Guide for Windows 11
Prerequisites Installation
1. Install Python (3.8 or higher)

Download Python from python.org
During installation, check "Add Python to PATH"
Verify installation: python --version

2. Install Git

Download Git from git-scm.com
Use default installation options

3. Install Ollama

Download Ollama from ollama.ai
Run the installer
Ollama will start automatically as a service

Step-by-Step Setup
Step 1: Create Project Directory
bashmkdir phidata-ollama-agent
cd phidata-ollama-agent
Step 2: Create Virtual Environment
bashpython -m venv venv
venv\Scripts\activate
Step 3: Install Required Packages
bashpip install phidata
pip install ollama
pip install requests
pip install python-dotenv
Step 4: Pull Ollama Model
bashollama pull llama2
# Or use other models like:
# ollama pull mistral
# ollama pull codellama
Step 5: Verify Ollama is Running
bashollama list
Project Structure
Create the following files in your project directory:
phidata-ollama-agent/
├── requirements.txt
├── setup_environment.py
├── ai_agent.py
├── .env
└── run_agent.py
File Contents
requirements.txt
phidata>=2.0.0
ollama>=0.1.0
requests>=2.31.0
python-dotenv>=1.0.0
.env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
setup_environment.py
pythonimport subprocess
import sys
import os
import requests
import time
from pathlib import Path

def run_command(command, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        return None

def check_python():
    """Check if Python is installed"""
    try:
        version = run_command("python --version")
        print(f"✓ Python found: {version}")
        return True
    except:
        print("✗ Python not found. Please install Python 3.8+")
        return False

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        # Check if Ollama is installed
        version = run_command("ollama --version")
        print(f"✓ Ollama found: {version}")
        
        # Check if Ollama service is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        print("✓ Ollama service is running")
        return True
    except requests.exceptions.RequestException:
        print("✗ Ollama service not running. Starting Ollama...")
        # Try to start Ollama
        subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(5)
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            print("✓ Ollama service started successfully")
            return True
        except:
            print("✗ Failed to start Ollama service")
            return False
    except:
        print("✗ Ollama not found. Please install Ollama from https://ollama.ai")
        return False

def check_virtual_environment():
    """Check if we're in a virtual environment"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment is active")
        return True
    else:
        print("✗ Virtual environment not active")
        return False

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        run_command("pip install -r requirements.txt")
        print("✓ Requirements installed successfully")
        return True
    except:
        print("✗ Failed to install requirements")
        return False

def check_ollama_model(model_name="llama2"):
    """Check if the specified model is available"""
    try:
        models = run_command("ollama list")
        if model_name in models:
            print(f"✓ Model '{model_name}' is available")
            return True
        else:
            print(f"Model '{model_name}' not found. Pulling model...")
            run_command(f"ollama pull {model_name}")
            print(f"✓ Model '{model_name}' pulled successfully")
            return True
    except:
        print(f"✗ Failed to check/pull model '{model_name}'")
        return False

def main():
    print("=== PhiData + Ollama Environment Setup ===\n")
    
    checks = [
        ("Python Installation", check_python),
        ("Ollama Installation & Service", check_ollama),
        ("Virtual Environment", check_virtual_environment),
        ("Package Installation", install_requirements),
        ("Ollama Model", lambda: check_ollama_model("llama2")),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\nChecking {check_name}...")
        if not check_func():
            all_passed = False
    
    print("\n=== Setup Summary ===")
    if all_passed:
        print("✓ All checks passed! Environment is ready.")
        print("\nYou can now run: python run_agent.py")
    else:
        print("✗ Some checks failed. Please resolve the issues above.")
    
    return all_passed

if __name__ == "__main__":
    main()
ai_agent.py
pythonimport os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.calculator import Calculator

# Load environment variables
load_dotenv()

class OllamaAgent:
    def __init__(self, model_name="llama2", base_url="http://localhost:11434"):
        """Initialize the Ollama-powered AI Agent"""
        self.model_name = model_name
        self.base_url = base_url
        
        # Initialize the Ollama model
        self.model = Ollama(
            id=model_name,
            base_url=base_url,
        )
        
        # Create the agent with tools
        self.agent = Agent(
            model=self.model,
            tools=[
                DuckDuckGo(),
                Calculator(),
            ],
            instructions=[
                "You are a helpful AI assistant powered by Ollama running locally.",
                "Use the available tools when needed to provide accurate information.",
                "Be concise but thorough in your responses.",
                "If you need to search for information, use the DuckDuckGo tool.",
                "For mathematical calculations, use the Calculator tool.",
            ],
            show_tool_calls=True,
            markdown=True,
        )
    
    def chat(self, message):
        """Send a message to the agent and get a response"""
        try:
            response = self.agent.run(message)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def start_interactive_session(self):
        """Start an interactive chat session"""
        print("=== PhiData + Ollama AI Agent ===")
        print(f"Model: {self.model_name}")
        print("Type 'quit' or 'exit' to end the session\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("Agent: ", end="")
                response = self.chat(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

def create_agent():
    """Factory function to create an agent"""
    model_name = os.getenv("OLLAMA_MODEL", "llama2")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    return OllamaAgent(model_name=model_name, base_url=base_url)

if __name__ == "__main__":
    agent = create_agent()
    agent.start_interactive_session()
run_agent.py
python#!/usr/bin/env python3
"""
Main script to run the PhiData + Ollama AI Agent
"""

import sys
import os
import requests
from ai_agent import create_agent

def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False

def main():
    print("Starting PhiData + Ollama AI Agent...\n")
    
    # Check if Ollama is running
    if not check_ollama_connection():
        print("❌ Ollama is not running or not accessible.")
        print("Please make sure Ollama is installed and running.")
        print("You can start it with: ollama serve")
        sys.exit(1)
    
    print("✅ Ollama connection verified")
    
    # Create and start the agent
    try:
        agent = create_agent()
        agent.start_interactive_session()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error starting agent: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
Usage Instructions
Initial Setup (Run Once)

Open Command Prompt or PowerShell as Administrator
Navigate to your project directory
Create virtual environment: python -m venv venv
Activate virtual environment: venv\Scripts\activate
Run setup script: python setup_environment.py

Daily Usage

Open Command Prompt or PowerShell
Navigate to your project directory
Activate virtual environment: venv\Scripts\activate
Run the agent: python run_agent.py

Automated Setup Script (setup.bat)
Create a setup.bat file for one-click setup:
batch@echo off
echo Setting up PhiData + Ollama AI Agent...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
pip install -r requirements.txt

REM Run setup check
python setup_environment.py

echo.
echo Setup complete! Run 'run.bat' to start the agent.
pause
Automated Run Script (run.bat)
Create a run.bat file for easy execution:
batch@echo off
call venv\Scripts\activate.bat
python run_agent.py
pause
Troubleshooting
Common Issues:

Ollama not found: Install from https://ollama.ai
Port 11434 in use: Restart Ollama service
Model not found: Run ollama pull [model-name]
Permission errors: Run Command Prompt as Administrator
Virtual environment issues: Delete venv folder and recreate

Checking Ollama Status:
bashollama list              # List installed models
ollama ps               # Show running models
ollama serve            # Start Ollama service manually
Available Models
Popular models you can use:

llama2 (7B) - Good general purpose
mistral (7B) - Fast and efficient
codellama (7B) - Good for coding tasks
llama2:13b - Larger, more capable
dolphin-mistral - Fine-tuned variant

Change the model in .env file or when creating the agent.
