from ai.groq_provider import GroqClient


system_prompt = """
You are a support assistant. I need you to give the intent of the user question. 
The intent can be one of the following: product_query, order_query, knowledge_query, or unknown.
Please respond with only the intent, without any additional text or explanation.
"""



client = GroqClient()


def detect_intent(user_input):
    """Detect the intent of the user question using Groq API"""
    response = client.generate(system_prompt, user_input)

    output = {"input": user_input, "intent": response.strip()}
    return output  # Return the intent without extra whitespace



if __name__ == "__main__":
    test_question = "good morning."
    intent = detect_intent(test_question)
    print(f"Detected intent: {intent}")