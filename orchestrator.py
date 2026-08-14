import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
from groq import Groq

from agents.planning_agent import PlanningAgent
from agents.designing_agent import DesigningAgent
from agents.creating_agent import CreatingAgent
from agents.testing_agent import TestingAgent

init(autoreset=True)
load_dotenv()

class Orchestrator:

    def __init__(self):
        print(Fore.CYAN + "\n" + "="*60)
        print(Fore.CYAN + "   Multi-Agent Code Generator - Starting Up...")
        print(Fore.CYAN + "="*60)

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            print(Fore.RED + "\n❌ ERROR: Groq API key missing!")
            print(Fore.YELLOW + "1. Go to https://console.groq.com")
            print(Fore.YELLOW + "2. Click API Keys → Create API Key")
            print(Fore.YELLOW + "3. Paste it in your .env file as GROQ_API_KEY=your_key")
            raise ValueError("Set GROQ_API_KEY in your .env file")

        print(Fore.GREEN + "✅ Groq API key loaded")

        self.client = Groq(api_key=api_key)
        self.model_name = "llama-3.3-70b-versatile"
        print(Fore.GREEN + f"✅ Model ready: {self.model_name}")

        self.planning_agent  = PlanningAgent(self.client, self.model_name)
        self.designing_agent = DesigningAgent(self.client, self.model_name)
        self.creating_agent  = CreatingAgent(self.client, self.model_name)
        self.testing_agent   = TestingAgent(self.client, self.model_name)
        print(Fore.GREEN + "✅ All 4 agents initialized")

        self.results = {}

    def run(self, user_request: str) -> dict:
        print(Fore.CYAN + f"\n  Processing: {user_request[:55]}...")
        print(Fore.CYAN + "="*60)

        print(Fore.YELLOW + "\n🔍 STEP 1/4 – Planning Agent...")
        self.results["plan"] = self.planning_agent.run(user_request)
        print(Fore.GREEN + "  ✅ Plan ready")

        print(Fore.YELLOW + "\n📐 STEP 2/4 – Designing Agent...")
        self.results["design"] = self.designing_agent.run(user_request, self.results["plan"])
        print(Fore.GREEN + "  ✅ Design ready")

        print(Fore.YELLOW + "\n💻 STEP 3/4 – Creating Agent...")
        self.results["code"] = self.creating_agent.run(user_request, self.results["plan"], self.results["design"])
        print(Fore.GREEN + "  ✅ Code ready")

        print(Fore.YELLOW + "\n🧪 STEP 4/4 – Testing Agent...")
        self.results["tests"] = self.testing_agent.run(user_request, self.results["code"])
        print(Fore.GREEN + "  ✅ Tests ready")

        print(Fore.GREEN + "\n🎉 All agents completed!")
        return self.results

    def display_results(self, results: dict):
        sections = [
            ("📋 PLAN",   results["plan"],   Fore.YELLOW),
            ("📐 DESIGN", results["design"], Fore.BLUE),
            ("💻 CODE",   results["code"],   Fore.MAGENTA),
            ("🧪 TESTS",  results["tests"],  Fore.CYAN),
        ]
        for title, content, color in sections:
            print(color + "\n" + "="*60)
            print(color + f"  {title}")
            print(color + "="*60)
            print(Style.RESET_ALL + content)
        print(Fore.GREEN + "\n✅ Done!")

    def save_results(self, results: dict, filename: str = "output"):
        path = f"{filename}.txt"
        with open(path, "w", encoding="utf-8") as f:
            for key, val in results.items():
                f.write(f"\n{'='*60}\n{key.upper()}\n{'='*60}\n{val}\n")
        print(Fore.GREEN + f"\n💾 Saved to: {path}")
        return path