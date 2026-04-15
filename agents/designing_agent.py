# agents/designing_agent.py
# =========================================
# DESIGNING AGENT
# =========================================

class DesigningAgent:
    """
    The Designing Agent creates software architecture
    from the given plan.
    """

    def __init__(self, model):
        self.model = model
        self.name = "Designing Agent"

        self.system_prompt = """You are an expert software architect agent.
Your ONLY job is to design the software architecture.

When given a plan, you must:
1. Define folder/file structure
2. Define classes and purpose
3. Define main functions
4. Explain data flow

Format:

ARCHITECTURE:

FOLDER STRUCTURE:
project/
├── file1.py
├── file2.py

CLASSES:
Class: Name
- Purpose:
- Methods:

FUNCTIONS:
def function():

DATA FLOW:
Explain flow

Do NOT write full code.
"""

    def run(self, user_request: str, plan: str) -> str:

        print(f"\n  [{self.name}] Designing architecture...")

        prompt = f"""
{self.system_prompt}

Original Request:
{user_request}

Development Plan:
{plan}
"""

        response = self.model.generate_content(prompt)

        return response.text