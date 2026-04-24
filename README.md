# online-shopping-agent 

An AI-powered shopping agent that autonomously searches Amazon and the web to find the best product within your budget — built with a Groq LLM (Llama 3.3 70B), Flask, and React.

## How It Works

1. You enter a product query and optional budget
2. The LLM **decides which tools to call** (Amazon API, web aggregator)
3. Results are **filtered for relevance** using LLM reasoning
4. The **best match is selected** and returned with source and price

```
User Query ──► LLM decides action ──► search_amazon / search_aggregator
                      │
                      ▼
              Filter by relevance (LLM)
                      │
                      ▼
              Choose best product (LLM)
                      │
                      ▼
                 Result Card
```

## Tech Stack

| Layer     | Tech                        |
|-----------|-----------------------------|
| Frontend  | React + Vite                |
| Backend   | Flask (Python)              |
| LLM       | Groq — Llama 3.3 70B        |
| Data      | RapidAPI (Amazon + Search)  |

## Project Structure

```
├── backend/
│   ├── app.py          # Flask API
│   ├── agent.py        # Agent loop + tools
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── SearchBar.jsx
│   │   │   ├── ProductCard.jsx
│   │   │   └── AgentSteps.jsx
│   └── package.json
├── .env.example
└── README.md
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/online-shopping-agent.git
cd online-shopping-agent
```

### 2. Create a `.env` file

```bash
cp .env.example .env
```

Fill in your keys:
- **GROQ_API_KEY** — get one free at [console.groq.com](https://console.groq.com)
- **RAPIDAPI_KEY** — subscribe to [Real-Time Amazon Data](https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-amazon-data) and [Real-Time Product Search](https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-product-search) on RapidAPI

### 3. Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Flask runs on `http://localhost:5000`.

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

React runs on `http://localhost:5173`. Open that URL in your browser.

## API

### `POST /api/search`

```json
{
  "query": "iPhone 14",
  "budget": 600
}
```

Response:

```json
{
  "product": {
    "title": "Apple iPhone 14 128GB",
    "price": 549.99,
    "rating": 4.7,
    "source": "amazon",
    "link": "https://..."
  },
  "steps": [
    { "step": 1, "action": "search_amazon", "found": 10 },
    { "step": 2, "action": "search_aggregator", "found": 8 }
  ]
}
```
