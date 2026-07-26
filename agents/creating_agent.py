# ========================================
# CREATING AGENT (FINAL SINGLE FILE - FIXED)
# ========================================

import google.generativeai as genai

# -----------------------------------------
# CREATING AGENT CLASS
# -----------------------------------------
class CreatingAgent:

    def __init__(self, model):
        self.model = model
        self.name = "Creating Agent"

    def run(self, user_request: str, plan: str, design: str) -> str:

        print(f"\n🔹 {self.name} is generating code...\n")

        prompt = f"""
You are an expert Python code generator.

Generate COMPLETE, WORKING Python code.

Rules:
1. Include all imports
2. Add comments
3. Use clean structure
4. Make it beginner-friendly

Format:

CODE:
```python
# filename.py

# full working code
EXPLANATION:
Explain the code simply

HOW TO RUN:
Steps to run

USER REQUEST:
{user_request}

PLAN:
{plan}

DESIGN:
{design}
"""