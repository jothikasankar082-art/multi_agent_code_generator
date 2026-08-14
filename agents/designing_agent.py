from groq import Groq

class DesigningAgent:
    def __init__(self, client: Groq, model_name: str):
        self.client = client
        self.model_name = model_name
        self.name = "Designing Agent"

    def run(self, user_request: str, plan: str) -> str:
        print(f"\n  [{self.name}] Designing architecture...")
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a software architect. Design folder structures, classes, and function signatures based on a plan. Do NOT write full implementation code."
                },
                {
                    "role": "user",
                    "content": f"Request: {user_request}\n\nPlan:\n{plan}\n\nDesign the folder structure, classes, and function signatures."
                }
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content