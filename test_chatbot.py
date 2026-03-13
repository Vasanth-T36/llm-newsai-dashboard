import sys
import os
import traceback

# Add current directory to path
sys.path.append(os.getcwd())

from ai_chatbot import ask_ai

def test_chatbot():
    print("Testing NewsAI Chatbot connection...")
    try:
        result = ask_ai(
            question="What is the current state of AI technology?",
            context="AI is evolving rapidly with new models like GPT-4.",
            chat_history=[],
            use_web_search=False,
            stream=False
        )

        print("\nAI Response received successfully.")
        print(f"Answer snippet: {result['answer'][:200]}...")
        
        if "error" in result['answer'].lower() or "timeout" in result['answer'].lower():
            print("\nChatbot test failed in response content.")
            print(f"Full Answer: {result['answer']}")
        else:
            print("\nChatbot test passed (Response content seems okay).")
            
    except Exception as e:
        print("\nAn error occurred during testing:")
        traceback.print_exc()

if __name__ == "__main__":
    test_chatbot()
