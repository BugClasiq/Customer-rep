import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from groq_provider import GroqClient
from intent_detector import detect_intent
from app import create_app
from app.extension import db
from app.models.product import Product
from app.models.order import Order
from app.models.knowledge_base import KnowledgeBase
import re


# System prompt for the AI assistant
ASSISTANT_SYSTEM_PROMPT = """
You are a helpful AI assistant for a store.
Your task is to answer user questions based ONLY on the provided context.

Rules:
1. Only answer questions about store-related topics: products, orders, policies, and store information.
2. Do NOT answer questions about anything else.
3. Base your answers only on the provided context data.
4. When prompting for order number: the format is in ORD followed by a set of number without any spaces in between them, so make sure you reconstruct it to that format if not provided in that way. you dont have to mention anything about the format to the user, this should be locale to you.
5. If you cannot find the answer in the context, say "I don't have information about that."
6. Be friendly and professional.
"""


class DatabaseRetriever:
    """Retrieves context from database based on intent"""
    
    @staticmethod
    def retrieve_product_context(user_input):
        """Retrieve product information from database"""
        products = Product.query.all()
        
        if not products:
            return "No products found matching your query."
        
        context = "Available Products:\n"
        for p in products:
            context += f"- {p.name}: ${p.price} ({p.category})\n  Description: {p.description}\n  In Stock: {p.quantity} units\n"
        return context
    
    @staticmethod
    def retrieve_order_context(user_input):
        """Retrieve order information from database"""

        order_number = re.search(r'ord\d+', user_input.lower())
        if order_number:
            # Try to find by order number first
            order = Order.query.filter(Order.order_number.ilike(f"%{order_number.group()}%")).first()
        else:
            order = None

        if not order:
            return "No order found. Please provide your order number."
        
        context = f"Order Information:\n"
        context += f"Order Number: {order.order_number}\n"
        context += f"Status: {order.status}\n"
        context += f"Total Amount: ${order.total_amount}\n"
        context += f"Delivery Address: {order.delivery_address}\n"
        context += f"Created: {order.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        
        if order.items:
            context += "Items:\n"
            for item in order.items:
                context += f"  - {item.product.name}: {item.quantity} x ${item.price}\n"
        
        return context
    
    @staticmethod
    def retrieve_knowledge_context(user_input):
        """Retrieve knowledge base information"""
        kb_items = KnowledgeBase.query.all()
        
        if not kb_items:
            return "No relevant information found in knowledge base."
        
        context = "Store Information:\n"
        for item in kb_items:
            context += f"- {item.title}: {item.content}\n"
        return context


def get_context_for_intent(intent, user_input):
    """Route to appropriate retrieval function based on intent"""
    intent_type = intent.lower().strip()
    
    if intent_type == "product_query":
        return DatabaseRetriever.retrieve_product_context(user_input)
    elif intent_type == "order_query":
        return DatabaseRetriever.retrieve_order_context(user_input)
    elif intent_type == "knowledge_query":
        return DatabaseRetriever.retrieve_knowledge_context(user_input)
    else:
        return "I can only help with questions about products, orders, or store policies."


def format_chat_history(chat_history):
    """Format previous exchanges into a single text block for the prompt."""
    if not chat_history:
        return ""

    formatted = "Chat History:\n"
    for item in chat_history:
        role = item.get("role", "user")
        message = item.get("message", "")
        formatted += f"{role.title()}: {message}\n"
    return formatted + "\n"


def generate_response(user_message, chat_history=None, app_context=None):
    """
    Main function to process user input and generate response
    
    Args:
        user_message: The user's input message
        chat_history: Optional list of previous messages
        app_context: Flask app context (optional, will be created if not provided)
    
    Returns:
        dict with keys: input, intent, context, response, chat_history
    """
    if chat_history is None:
        chat_history = []

    # Detect intent
    intent_result = detect_intent(user_message)
    intent = intent_result["intent"]
    
    # Create app context if not provided
    if app_context is None:
        app = create_app()
        app_context = app.app_context()
    
    # Retrieve relevant context from database
    with app_context:
        context = get_context_for_intent(intent, user_message)
    
    # Build messages for LLM
    history_text = format_chat_history(chat_history)
    full_prompt = f"""
{ASSISTANT_SYSTEM_PROMPT}

{history_text}Context from Database:
{context}

User Question: {user_message}

Assistant Response:
"""
    
    # Generate response using Groq
    client = GroqClient()
    response = client.generate(ASSISTANT_SYSTEM_PROMPT, full_prompt).strip()
    
    # Update chat history
    chat_history.append({"role": "user", "message": user_message})
    chat_history.append({"role": "assistant", "message": response})
    
    return {
        "input": user_message,
        "intent": intent,
        "context": context,
        "response": response,
        "chat_history": chat_history
    }


if __name__ == "__main__":
    # Simulate a continuous chat
    chat_history = []


    while True:
        user_message= input("User: ")
        if user_message.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

    
        result = generate_response(user_message, chat_history=chat_history)
        # print(f"User: {result['input']}")
        # print(f"Intent: {result['intent']}")
        print(f"Assistant: {result['response']}\n")

    # print("Final chat history:")
    # for item in chat_history:
    #     print(f"{item['role'].title()}: {item['message']}")