
from groq import Groq
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(basedir, ".env"))
load_dotenv()



class GroqClient:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("API key is required for GroqClient.")
        client = Groq(api_key=self.api_key)
        
        completion = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                temperature=1,
                max_completion_tokens=2048,
                top_p=1,
                stream=False,
            )
        return completion.choices[0].message.content
    

if __name__ == "__main__":
    client = GroqClient()
    system_prompt = "You are a helpful assistant."
    user_prompt = "What is the capital of France?"
    response = client.generate(system_prompt, user_prompt)
    print("Response from Groq API:", response)