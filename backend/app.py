from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from agent import run_agent

load_dotenv(dotenv_path="../.env")

app = Flask(__name__)
CORS(app)


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json(force=True)
    query = (data.get("query") or "").strip()
    budget = data.get("budget")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        product, steps = run_agent(query, budget)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if product is None:
        return jsonify({"error": "No relevant products found within your budget"}), 404

    return jsonify({"product": product, "steps": steps})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
