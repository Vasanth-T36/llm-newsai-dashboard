import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from web_search import search_web

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"


SYSTEM_PROMPT = """You are NewsAI — an elite, highly knowledgeable AI news analyst and assistant.
Current time: {now}

Your capabilities:
- Deep analysis of breaking news and global events
- Sentiment analysis and bias detection in news articles
- Connecting news stories across different topics and regions
- Providing historical context and background information
- Predicting potential implications of current events
- Fact-checking claims against provided news context
- Generating concise, insightful summaries

Personality: You are sharp, articulate, and neutral. You present multiple perspectives when covering controversial topics. You always cite sources from the provided context. You proactively suggest related angles and follow-up questions.

Guidelines:
1. Always base your answers on the provided news context when available
2. Clearly distinguish between facts from the news and your analysis
3. Mention publication dates of sources when relevant
4. Highlight if a question cannot be answered from the provided context
5. Use bullet points and headers for complex answers
6. Offer follow-up questions the user might find interesting
7. If asked to search the web, use the web_search results provided
"""

def build_messages(question: str, context: str, chat_history: list, web_results: list = None) -> list:
    """Build full message chain including conversation history."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Build enriched context
    full_context = f"=== NEWS CONTEXT ===\n{context}\n"
    
    if web_results:
        full_context += "\n=== WEB SEARCH RESULTS ===\n"
        for r in web_results:
            full_context += f"Title: {r['title']}\nSnippet: {r['snippet']}\nLink: {r['link']}\n\n"
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(now=now)}
    ]
    
    # Add conversation history (keep last 10 exchanges for context)
    history_to_include = chat_history[-10:] if len(chat_history) > 10 else chat_history
    for msg in history_to_include:
        messages.append({"role": "user", "content": msg["question"]})
        messages.append({"role": "assistant", "content": msg["answer"]})
    
    # Add current question with context
    user_message = f"{full_context}\n\n=== CURRENT QUESTION ===\n{question}"
    messages.append({"role": "user", "content": user_message})
    
    return messages


def ask_ai(question: str, context: str, chat_history: list = None, use_web_search: bool = False, stream: bool = True):
    """
    Full AI response with optional web search, returns structured response or generator.
    """
    if chat_history is None:
        chat_history = []
    
    web_results = []
    if use_web_search:
        try:
            web_results = search_web(question, max_results=5)
        except Exception:
            web_results = []
    
    messages = build_messages(question, context, chat_history, web_results)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://news-ai-dashboard.app",
        "X-Title": "NewsAI Dashboard"
    }
    
    data = {
        "model": "openai/gpt-4o-mini",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1500,
        "stream": stream
    }
    
    if not stream:
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            answer = result["choices"][0]["message"]["content"]
            return {
                "answer": answer,
                "web_searched": use_web_search and len(web_results) > 0,
                "web_result_count": len(web_results),
            }
        except Exception as e:
            return {"answer": f"❌ Error: {str(e)}", "web_searched": False}

    # Streaming logic
    def generate():
        full_answer = ""
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=30, stream=True)
            response.raise_for_status()
            
            import json
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        content = line_str[6:]
                        if content == '[DONE]':
                            break
                        try:
                            chunk = json.loads(content)
                            delta = chunk['choices'][0]['delta'].get('content', '')
                            full_answer += delta
                            yield delta
                        except Exception:
                            continue
        except Exception as e:
            yield f"❌ Connection Error: {str(e)}"
        
    return generate(), use_web_search and len(web_results) > 0


def get_follow_up_suggestions(question: str, answer: str) -> list:
    """Generate follow-up question suggestions (Fast recovery if it fails)."""
    # Quick defaults to avoid blocking if the API is slow
    default_qs = [
        "Can you explain more about this?",
        "What are the global implications?",
        "Are there any updates on this?"
    ]
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": f"Generate exactly 3 short follow-up questions (max 8 words each) based on the news conversation. Return ONLY a JSON array."
            },
            {
                "role": "user",
                "content": f"Q: {question}\nA: {answer[:300]}..."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=5) # Tight timeout for speed
        import json
        content = response.json()["choices"][0]["message"]["content"].strip()
        # Strip potential markdown code blocks
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
        questions = json.loads(content)
        return questions[:3] if isinstance(questions, list) else default_qs
    except Exception:
        return default_qs


def analyze_sentiment(text: str) -> dict:
    """Quick sentiment analysis of a news piece."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Analyze the sentiment. Reply with ONLY a JSON: {\"sentiment\": \"positive/negative/neutral\", \"score\": 0-100, \"emoji\": \"😊/😟/😐\"}"
            },
            {"role": "user", "content": text[:500]}
        ],
        "temperature": 0.1,
        "max_tokens": 60
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=10)
        import json
        content = response.json()["choices"][0]["message"]["content"].strip()
        return json.loads(content)
    except Exception:
        return {"sentiment": "neutral", "score": 50, "emoji": "😐"}