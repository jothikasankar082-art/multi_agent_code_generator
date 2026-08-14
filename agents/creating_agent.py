from groq import Groq

class CreatingAgent:
    def __init__(self, client: Groq, model_name: str):
        self.client = client
        self.model_name = model_name
        self.name = "Creating Agent"

    def run(self, user_request: str, plan: str, design: str) -> str:
        print(f"\n  [{self.name}] Writing the code...")
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python developer. Write complete, working, well-commented Python code. Include all imports. Include instructions on how to run it."
                },
                {
                    "role": "user",
                    "content": f"Request: {user_request}\n\nPlan:\n{plan}\n\nDesign:\n{design}\n\nWrite the complete working Python code."
                }
            ],
            temperature=0.3,
            max_tokens=8192,
        )
        return response.choices[0].message.content