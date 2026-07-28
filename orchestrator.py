# =========================================
# ORCHESTRATOR (FINAL CORRECT VERSION)
# =========================================

import google.generativeai as genai
from colorama import Fore, Style, init

# Import agents
from agents.planning_agent import PlanningAgent
from agents.designing_agent import DesigningAgent
from agents.creating_agent import CreatingAgent
from agents.testing_agent import TestingAgent

# Initialize colorama
init(autoreset=True)


class Orchestrator:

    def __init__(self):

        print(Fore.CYAN + "\n" + "="*60)
        print(Fore.CYAN + "   Multi-Agent Code Generator - Starting Up...")
        print(Fore.CYAN + "="*60)

        # ✅ STEP 1: Set API Key (Direct - no .env issues)
        api_key = "OPENAI_API_KEY"
        print(Fore.GREEN + "✅ API Key loaded successfully")

        # ✅ STEP 2: Configure Gemini
        genai.configure(api_key=api_key)

        # ✅ STEP 3: Create model
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        print(Fore.GREEN + "✅ Gemini model loaded")

        # ✅ STEP 4: Initialize all agents
        self.planning_agent  = PlanningAgent(self.model)
        self.designing_agent = DesigningAgent(self.model)
        self.creating_agent  = CreatingAgent(self.model)
        self.testing_agent   = TestingAgent(self.model)

        print(Fore.GREEN + "✅ All agents initialized")

        # Store results
        self.results = {}

    def run(self, user_request):

        print(Fore.CYAN + "\nProcessing...\n")

        # Step 1: Planning
        print(Fore.YELLOW + "🔹 Planning...")
        self.results["plan"] = self.planning_agent.run(user_request)

        # Step 2: Designing
        print(Fore.YELLOW + "🔹 Designing...")
        self.results["design"] = self.designing_agent.run(
            user_request,
            self.results["plan"]
        )

        # Step 3: Creating
        print(Fore.YELLOW + "🔹 Creating...")
        self.results["code"] = self.creating_agent.run(
            user_request,
            self.results["plan"],
            self.results["design"]
        )

        # Step 4: Testing
        print(Fore.YELLOW + "🔹 Testing...")
        self.results["tests"] = self.testing_agent.run(
            user_request,
            self.results["code"]
        )

        print(Fore.GREEN + "\n✅ All steps completed!")

        return self.results

    def display_results(self, results):

        print("\n" + "="*60)

        print("\n📋 PLAN:\n", results["plan"])
        print("\n📐 DESIGN:\n", results["design"])
        print("\n💻 CODE:\n", results["code"])
        print("\n🧪 TEST:\n", results["tests"])

        print("\n" + "="*60)

    def save_results(self, results, filename="output.txt"):

        with open(filename, "w", encoding="utf-8") as f:
            for key, value in results.items():
                f.write(f"\n==== {key.upper()} ====\n")
                f.write(value + "\n")

        print(Fore.GREEN + f"\n💾 Saved to {filename}")


# =========================================
# MAIN
# =========================================
if __name__ == "__main__":

    orchestrator = Orchestrator()

user_request = input("\n💡 Enter what you want to build: ")

    results = orchestrator.run(user_request)

    orchestrator.display_results(results)

    orchestrator.save_results(results)
