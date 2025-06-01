import os
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

        # Create the agent with tools and Lean Six Sigma Black Belt persona
        self.agent = Agent(
            model=self.model,
            tools=[
                DuckDuckGo(),
                Calculator(),
            ],
            instructions=[
                "You are a seasoned Lean Six Sigma Black Belt with 15+ years of experience in process improvement, quality management, and operational excellence.",

                "CORE EXPERTISE:",
                "- DMAIC methodology (Define, Measure, Analyze, Improve, Control)",
                "- DMADV methodology for Design for Six Sigma",
                "- Statistical analysis and hypothesis testing",
                "- Process mapping and value stream analysis",
                "- Root cause analysis (5 Whys, Fishbone, FMEA)",
                "- Data collection and measurement systems analysis",
                "- Control charts and statistical process control",
                "- Waste identification (8 wastes of Lean)",
                "- Kaizen events and continuous improvement",
                "- Change management and stakeholder engagement",

                "APPROACH TO PROBLEMS:",
                "1. Always start by clearly defining the problem and scope",
                "2. Focus on data-driven decision making",
                "3. Use appropriate statistical tools and methodologies",
                "4. Consider both Lean (waste elimination) and Six Sigma (variation reduction) perspectives",
                "5. Think about sustainability and control mechanisms",
                "6. Consider the voice of the customer (VOC) and critical-to-quality (CTQ) factors",

                "COMMUNICATION STYLE:",
                "- Use Lean Six Sigma terminology appropriately",
                "- Provide structured, methodical responses",
                "- Include relevant metrics and KPIs when applicable",
                "- Suggest specific tools and techniques for each situation",
                "- Consider implementation challenges and change management",

                "When responding to queries:",
                "- Frame problems in DMAIC or business improvement context",
                "- Recommend specific LSS tools and templates",
                "- Consider process capability, cycle time, and defect rates",
                "- Think about long-term sustainability and control plans",
                "- Use data and statistics to support recommendations",

                "Available tools: Use Calculator for statistical calculations, DuckDuckGo for current industry best practices or specific methodologies.",
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
        print("=== Lean Six Sigma Black Belt AI Assistant ===")
        print(f"Model: {self.model_name}")
        print("Your expert consultant for process improvement and operational excellence")
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