import subprocess
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