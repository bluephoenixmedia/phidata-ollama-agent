import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.calculator import Calculator

# Load environment variables
load_dotenv()


class LeanSixSigmaAgent:
    def __init__(self, model_name="llama2", base_url="http://localhost:11434"):
        """Initialize the Lean Six Sigma Black Belt AI Agent"""
        self.model_name = model_name
        self.base_url = base_url

        # Initialize the Ollama model
        self.model = Ollama(
            id=model_name,
            base_url=base_url,
        )

        # Create the specialized Lean Six Sigma agent
        self.agent = Agent(
            model=self.model,
            tools=[
                DuckDuckGo(),
                Calculator(),
            ],
            instructions=[
                "You are Master Black Belt Sarah Chen, a seasoned Lean Six Sigma expert with 18+ years of experience across manufacturing, healthcare, financial services, and technology sectors.",

                "PROFESSIONAL BACKGROUND:",
                "- Master Black Belt certification (ASQ, IASSC)",
                "- Led 200+ improvement projects with combined savings of $50M+",
                "- Expertise in Change Management, Project Management (PMP), and Statistical Analysis",
                "- Industry experience: Automotive, Aerospace, Healthcare, Banking, IT/Software",
                "- Trained 150+ Green Belts and 45+ Black Belts",

                "CORE METHODOLOGIES & TOOLS:",
                "DMAIC Framework:",
                "- Define: Project Charter, SIPOC, VOC, CTQ Tree, Stakeholder Analysis",
                "- Measure: Data Collection Plan, MSA, Process Capability, Baseline Metrics",
                "- Analyze: Root Cause Analysis (5 Whys, Fishbone, FMEA), Statistical Analysis, Hypothesis Testing",
                "- Improve: Solution Design, Pilot Planning, Cost-Benefit Analysis, Implementation Planning",
                "- Control: Control Plan, SPC, Mistake-Proofing, Standardization",

                "LEAN TOOLS:",
                "- 8 Wastes (TIMWOODS): Transportation, Inventory, Motion, Waiting, Overprocessing, Overproduction, Defects, Skills",
                "- Value Stream Mapping, Kaizen Events, 5S, Kanban, Takt Time, Flow Analysis",
                "- Standard Work, Quick Changeover (SMED), Total Productive Maintenance (TPM)",

                "STATISTICAL EXPERTISE:",
                "- Descriptive Statistics, Hypothesis Testing (t-tests, ANOVA, Chi-square)",
                "- Regression Analysis, DOE (Design of Experiments), Control Charts",
                "- Process Capability Studies (Cp, Cpk, Pp, Ppk), Measurement Systems Analysis",
                "- Statistical Software: Minitab, JMP, R, Excel Analytics",

                "PROBLEM-SOLVING APPROACH:",
                "1. Always start with business impact and customer value",
                "2. Use data to drive every decision - 'In God we trust, all others bring data'",
                "3. Apply appropriate statistical rigor based on problem complexity",
                "4. Consider both short-term fixes and long-term systematic solutions",
                "5. Focus on sustainable improvements with robust control systems",
                "6. Engage stakeholders throughout the process",
                "7. Calculate ROI and business impact of all recommendations",

                "COMMUNICATION STYLE:",
                "- Lead with business impact and customer value",
                "- Use structured problem-solving frameworks",
                "- Provide specific, actionable recommendations",
                "- Include implementation timelines and resource requirements",
                "- Address potential risks and mitigation strategies",
                "- Suggest appropriate metrics and control mechanisms",
                "- Reference relevant case studies and best practices",

                "RESPONSE FRAMEWORK:",
                "For any problem or question:",
                "1. Clarify the problem statement and scope",
                "2. Identify relevant LSS methodology (DMAIC, Kaizen, etc.)",
                "3. Recommend specific tools and techniques",
                "4. Provide step-by-step implementation guidance",
                "5. Suggest metrics for tracking progress",
                "6. Address sustainability and control considerations",
                "7. Estimate timeline and resource requirements",

                "Use Calculator for statistical calculations and DuckDuckGo for current industry benchmarks or specific methodology updates.",
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

    def provide_dmaic_template(self):
        """Provide a DMAIC project template"""
        template = """
# DMAIC Project Template

## DEFINE Phase
- [ ] Problem Statement
- [ ] Project Charter (Business Case, Scope, Goals, Timeline)
- [ ] SIPOC Diagram
- [ ] Voice of Customer (VOC) Analysis
- [ ] Critical to Quality (CTQ) Tree
- [ ] Stakeholder Analysis
- [ ] Team Formation

## MEASURE Phase
- [ ] Data Collection Plan
- [ ] Operational Definitions
- [ ] Measurement System Analysis (MSA)
- [ ] Baseline Data Collection
- [ ] Process Capability Assessment
- [ ] Current State Process Map

## ANALYZE Phase
- [ ] Data Analysis & Visualization
- [ ] Root Cause Analysis (5 Whys, Fishbone)
- [ ] Failure Mode & Effects Analysis (FMEA)
- [ ] Statistical Analysis & Hypothesis Testing
- [ ] Value Stream Analysis
- [ ] Gap Analysis

## IMPROVE Phase
- [ ] Solution Generation & Evaluation
- [ ] Pilot Planning & Execution
- [ ] Cost-Benefit Analysis
- [ ] Risk Assessment & Mitigation
- [ ] Implementation Planning
- [ ] Training & Change Management

## CONTROL Phase
- [ ] Control Plan Development
- [ ] Statistical Process Control (SPC)
- [ ] Standard Operating Procedures
- [ ] Training & Documentation
- [ ] Mistake-Proofing (Poka-Yoke)
- [ ] Project Closure & Handoff
        """
        return template

    def start_interactive_session(self):
        """Start an interactive LSS consultation session"""
        print("=" * 60)
        print("🎯 LEAN SIX SIGMA BLACK BELT CONSULTANT")
        print("   Master Black Belt Sarah Chen - AI Assistant")
        print("=" * 60)
        print(f"Model: {self.model_name}")
        print("\n🔧 Specializing in:")
        print("  • Process Improvement & Optimization")
        print("  • Quality Management & Defect Reduction")
        print("  • Statistical Analysis & Data-Driven Solutions")
        print("  • Change Management & Project Leadership")
        print("\n💡 Quick Commands:")
        print("  'dmaic' - Get DMAIC project template")
        print("  'tools' - List available LSS tools")
        print("  'quit' or 'exit' - End session")
        print("\n" + "─" * 60)

        while True:
            try:
                user_input = input("\n🤔 Your Challenge: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n✅ Remember: Continuous improvement is a journey, not a destination!")
                    print("   Keep measuring, analyzing, and improving!")
                    break

                if user_input.lower() == 'dmaic':
                    print("\n📋 DMAIC PROJECT TEMPLATE:")
                    print(self.provide_dmaic_template())
                    continue

                if user_input.lower() == 'tools':
                    tools_list = """
🛠️ LEAN SIX SIGMA TOOLKIT:

DEFINE: Project Charter, SIPOC, VOC, CTQ Tree, Stakeholder Analysis
MEASURE: MSA, Process Capability, Data Collection Plans, Baseline Metrics  
ANALYZE: 5 Whys, Fishbone, FMEA, Hypothesis Testing, Pareto Charts
IMPROVE: DOE, Pilot Plans, Cost-Benefit Analysis, Solution Design
CONTROL: Control Charts, SPC, Standard Work, Poka-Yoke

LEAN TOOLS: VSM, Kaizen, 5S, Kanban, SMED, Takt Time Analysis
STATISTICAL: t-tests, ANOVA, Regression, Control Charts, Cp/Cpk
                    """
                    print(tools_list)
                    continue

                if not user_input:
                    continue

                print("\n🎯 LSS Analysis:")
                print("─" * 40)
                response = self.chat(user_input)
                print(response)

            except KeyboardInterrupt:
                print("\n\n✅ Session ended. Keep improving!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")


def create_lss_agent():
    """Factory function to create a Lean Six Sigma agent"""
    model_name = os.getenv("OLLAMA_MODEL", "llama2")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    return LeanSixSigmaAgent(model_name=model_name, base_url=base_url)


if __name__ == "__main__":
    agent = create_lss_agent()
    agent.start_interactive_session()