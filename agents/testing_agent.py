from groq import Groq

class TestingAgent:
    def __init__(self, client: Groq, model_name: str):
        self.client = client
        self.model_name = model_name
        self.name = "Testing Agent"

    def run(self, user_request: str, code: str) -> str:
        print(f"\n  [{self.name}] Reviewing code and writing tests...")
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a QA engineer. Review Python code for bugs and improvements. Write pytest test cases. Give a final verdict: Excellent, Good, or Needs Work."
                },
                {
                    "role": "user",
                    "content": f"Request: {user_request}\n\nCode:\n{code}\n\nReview the code and write pytest test cases."
                }
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content