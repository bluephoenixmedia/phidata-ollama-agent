#!/usr/bin/env python3
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