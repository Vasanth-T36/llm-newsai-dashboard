# NewsAI — Real-Time Intelligence Dashboard

NewsAI is a high-performance, full-stack AI-powered news dashboard designed to fetch, summarize, and analyze global news in real-time. It combines a premium glassmorphic UI with advanced Natural Language Processing (NLP) and a deep-search AI Assistant to provide users with a comprehensive overview of current events.

---

## Key Features

### Real-Time News Engine
*   **Global & Regional Feeds**: Fetch news from tailored regions (India, US, UK, etc.) based on Google News RSS.
*   **Intelligent Summarization**: Automatically extracts and summarizes articles using NLTK and Newspaper3k.
*   **Sentiment Detection**: AI-powered sentiment analysis (😊 Positive, 😟 Negative, 😐 Neutral) for every news card.
*   **Persistent Storage**: Efficiently stores fetched headlines and metadata in a local SQLite database.

### Advanced AI Chatbot (NewsAI)
*   **RAG (Retrieval-Augmented Generation)**: Uses FAISS vector search to answer questions based on the live news feed.
*   **Web Search Integration**: Seamlessly searches the live web via DuckDuckGo for context beyond the current feed.
*   **Contextual Memory**: Remembers conversation history for deep, iterative analysis.
*   **Proactive Insights**: Suggests follow-up questions and provides detailed citations/sources.

### Premium UI/UX
*   **Glassmorphic Design**: Modern dark-mode interface with translucent elements and smooth CSS animations.
*   **Interactive Stats**: Real-time metrics on articles loaded, AI interactions, and system status.
*   **Two-Panel Layout**: Seamlessly switch between the live news feed and the AI workspace.

---

## Project Structure

```text
NLP_News_Project/
├── app.py                # Main Streamlit application (UI & Logic)
├── ai_chatbot.py         # AI Logic (RAG, Web Search, Sentiment)
├── news_fetcher.py       # RSS News Fetching module
├── vector_store.py       # Vector DB management (FAISS)
├── database.py           # SQLite persistent storage logic
├── article_extractor.py  # Article scraping (Newspaper3k)
├── summarizer.py         # Text summarization (NLTK)
├── web_search.py         # DuckDuckGo integration
├── requirements.txt      # Project dependencies
└── README.md             # Documentation
```

---

## Tech Stack

### Frontend & UI
*   **Streamlit**: Core application framework.
*   **Custom CSS3**: Premium glassmorphism, animations, and typography (Inter & Space Grotesk).
*   **HTML5/Markdown**: Rich content rendering.

### Backend & AI
*   **GPT-4o-mini (OpenRouter)**: Analytical brain for chat and sentiment analysis.
*   **FAISS**: Vector database for lightning-fast semantic search.
*   **Sentence-Transformers**: High-quality embeddings (`all-MiniLM-L6-v2`).
*   **SQLite**: Local relational database for metadata persistence.
*   **Newspaper3k & NLTK**: Article extraction and linguistic processing.
*   **DuckDuckGo Search**: Real-time web search capabilities.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/NLP_News_Project.git
cd NLP_News_Project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize NLTK Data
The summarizer requires the `punkt` tokenizer. Run the following in Python:
```python
import nltk
nltk.download('punkt')
```

### 4. Configure API Key
Create a `.env` file in the root directory and add your OpenRouter API Key:
```env
OPENROUTER_API_KEY=your_openrouter_api_key
```


### 5. Run the Application
```bash
streamlit run app.py
```

---

## Usage Guide

1.  **Select Region**: Use the sidebar to focus on specific news markets (e.g., India, Global).
2.  **Explore Feed**: Browse news cards, check sentiment tags, and click links for original sources.
3.  **Chat with NewsAI**: Ask questions about specific events. Toggle **"Search the web too"** for broader context.
4.  **Instant Refresh**: Use the "Refresh" button to pull the latest headlines and update the dashboard.

---


