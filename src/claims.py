import os
from llm import ask_json

SYSTEM = """You find factual claims in an AI-written answer that could become outdated.
Time-sensitive means: prices, version numbers, API features, laws, rules, company leaders,
statistics, 'latest' or 'current' statements.
Return ONLY JSON in this form:
{"claims": [{"claim": "exact short claim", "type": "pricing|version|law|leadership|stat|other", "search_query": "short web search query"}]}
Ignore timeless facts. Return at most 8 claims."""

def extract_claims(answer):
    data = ask_json(os.getenv("CHEAP_MODEL"), SYSTEM, answer)
    return data["claims"]

if __name__ == "__main__":
    sample = "Python 3.9 is the latest version. The CEO of Twitter is Jack Dorsey."
    for c in extract_claims(sample):
        print(c)