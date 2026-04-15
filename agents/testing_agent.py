# agents/testing_agent.py
# =========================================
# TESTING AGENT
# =========================================

class TestingAgent:

    def __init__(self, model):
        self.model = model
        self.name = "Testing Agent"

    def run(self, user_request: str, code: str) -> str:

        print(f"\n  [{self.name}] Testing code...")

        prompt = f"""
You are a Testing Agent.

Check the given Python code.

USER REQUEST:
{user_request}

CODE:
{code}

Tasks:
1. Find bugs
2. Suggest improvements
3. Provide corrected code if needed
"""

        response = self.model.generate_content(prompt)

        return response.text