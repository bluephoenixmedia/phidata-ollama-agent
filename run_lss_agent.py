#!/usr/bin/env python3
"""
Script to run the specialized Lean Six Sigma Black Belt AI Agent
"""

import sys
import os
import requests
from lss_agent import create_lss_agent


def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False


def main():
    print("Initializing Lean Six Sigma Black Belt Consultant...\n")

    # Check if Ollama is running
    if not check_ollama_connection():
        print("❌ Ollama is not running or not accessible.")
        print("Please make sure Ollama is installed and running.")
        print("You can start it with: ollama serve")
        sys.exit(1)

    print("✅ System ready - Connecting to LSS expertise base...")

    # Create and start the specialized agent
    try:
        agent = create_lss_agent()
        agent.start_interactive_session()
    except KeyboardInterrupt:
        print("\nShutting down LSS consultant...")
    except Exception as e:
        print(f"Error starting LSS agent: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()