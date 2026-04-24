import requests
from groq import Groq
import os
import json


def _get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")
    return Groq(api_key=api_key)


_client = None


def _client_instance():
    global _client
    if _client is None:
        _client = _get_client()
    return _client


def call_llm(prompt, expect_json=False):
    response = _client_instance().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.choices[0].message.content.strip()

    if expect_json:
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])
        except Exception:
            return {"action": "FINISH"}

    return text


def search_amazon_tool(query):
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
    }
    res = requests.get(
        "https://real-time-amazon-data.p.rapidapi.com/search",
        headers=headers,
        params={"query": query, "page": "1", "country": "US"},
    ).json()

    cleaned = []
    for p in res.get("data", {}).get("products", [])[:10]:
        try:
            price = float(p.get("product_price", "0").replace("$", "").replace(",", ""))
        except Exception:
            price = 0
        cleaned.append({
            "title": p.get("product_title"),
            "price": price,
            "rating": float(p.get("product_star_rating") or 0),
            "source": "amazon",
            "link": p.get("product_url"),
        })
    return cleaned


def search_aggregator_tool(query):
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": "real-time-product-search.p.rapidapi.com",
    }
    res = requests.get(
        "https://real-time-product-search.p.rapidapi.com/search-v2",
        headers=headers,
        params={"q": query, "country": "us", "limit": "10"},
    ).json()

    cleaned = []
    for p in res.get("data", {}).get("products", [])[:10]:
        offer = p.get("offer") or {}
        try:
            price = float(offer.get("price", "0").replace("$", "").replace(",", ""))
        except Exception:
            price = 0
        cleaned.append({
            "title": p.get("product_title"),
            "price": price,
            "rating": 0,
            "source": "aggregator",
            "link": offer.get("offer_page_url"),
        })
    return cleaned


def decide_next_action(query, history):
    prompt = f"""You are an AI shopping agent.

Goal: Find the best product for: "{query}"

Available tools:
- search_amazon
- search_aggregator

History:
{json.dumps(history)}

Rules:
- If you don't have enough results, call a tool
- If you have enough data, return FINISH

Return ONLY JSON:
{{"action": "search_amazon | search_aggregator | FINISH"}}"""
    return call_llm(prompt, expect_json=True)


def is_relevant(title, query):
    prompt = f"""Query: {query}
Product: {title}

Is this the MAIN product the user wants? Answer ONLY: YES or NO"""
    return "YES" in call_llm(prompt).upper()


def choose_best(products, query):
    prompt = f"""Query: {query}

Products:
{json.dumps(products, indent=2)}

Select the BEST product. Return ONLY the index number (0, 1, 2, ...)."""
    try:
        return products[int(call_llm(prompt).strip())]
    except Exception:
        return products[0]


def run_agent(query, budget=None):
    history = []
    all_results = []
    steps = []

    for step_num in range(5):
        decision = decide_next_action(query, history)
        action = decision.get("action", "FINISH")

        if action == "FINISH":
            break
        elif action == "search_amazon":
            results = search_amazon_tool(query)
        elif action == "search_aggregator":
            results = search_aggregator_tool(query)
        else:
            break

        all_results.extend(results)
        history.append({"action": action, "results": len(results)})
        steps.append({"step": step_num + 1, "action": action, "found": len(results)})

    if budget is not None:
        all_results = [p for p in all_results if p["price"] <= budget]

    relevant = [p for p in all_results if is_relevant(p["title"], query)]

    if not relevant:
        return None, steps

    return choose_best(relevant, query), steps
