from groq import Groq

class PlanningAgent:
    def __init__(self, client: Groq, model_name: str):
        self.client = client
        self.model_name = model_name
        self.name = "Planning Agent"

    def run(self, user_request: str) -> str:
        print(f"\n  [{self.name}] Creating plan...")
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a software planning expert. Create clear numbered development plans. List technologies needed. Do NOT write any code."
                },
                {
                    "role": "user",
                    "content": f"Create a step-by-step development plan for: {user_request}"
                }
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content