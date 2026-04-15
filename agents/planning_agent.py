# agents/planning_agent.py
# =========================================
# PLANNING AGENT
# Role: Breaks the user's request into a clear,
#       step-by-step development plan.
# =========================================

class PlanningAgent:
    """
    The Planning Agent is the FIRST agent to run.
    It reads the user's request and creates a development plan.
    """

    def __init__(self, model):
        self.model = model
        self.name = "Planning Agent"

        # System prompt
        self.system_prompt = """You are an expert software planning agent. 
Your ONLY job is to create a clear, numbered development plan.

When given a coding request, you must:
1. Understand what needs to be built
2. Break it down into 4-6 clear steps
3. List technologies/libraries needed
4. Identify challenges

Format your response as:

PLAN:
Step 1: ...
Step 2: ...

TECHNOLOGIES:
- ...

CHALLENGES:
- ...

Do NOT write any code.
"""

    def run(self, user_request: str) -> str:
        """
        Takes the user's request and returns a development plan.
        """

        print(f"\n  [{self.name}] Creating plan...")

        # Combine system prompt + user request
        prompt = f"""
{self.system_prompt}

User Request:
{user_request}
"""

        # Call Gemini model
        response = self.model.generate_content(prompt)

        return response.text