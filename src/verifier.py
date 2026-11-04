import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables
load_dotenv()

# 2. Configure OpenAI client to talk to local Ollama
client = OpenAI(
    base_url=os.getenv("BIFROST_BASE_URL"),
    api_key=os.getenv("OPENROUTER_API_KEY") # Just a placeholder for Ollama
)

STRONG_MODEL = os.getenv("STRONG_MODEL", "llama3.2")

# 3. The Judge Prompt
VERIFICATION_PROMPT = """
You are an expert fact-checker. Your job is to compare a specific claim against recent web search results and determine its current validity.

Claim to check: "{claim}"

Recent Search Results:
{search_results}

Based on the search results, output ONLY a valid JSON object with exactly these three keys:
- "status": (string) Must be exactly one of: "Still true", "Outdated", or "Cannot verify"
- "reason": (string) A short, 1-sentence explanation of why.
- "freshness_score": (integer) A score from 0 to 100. 
   - 90-100: Search results strongly confirm the claim with recent, authoritative sources.
   - 40-89: Claim is partially true, outdated, or sources are mixed/older.
   - 0-39: Claim is completely contradicted by recent sources (e.g., a CEO changed, price changed).

Example output:
{{
  "status": "Outdated",
  "reason": "Search results confirm Jack Dorsey stepped down in 2021 and was replaced, and later Elon Musk acquired the company.",
  "freshness_score": 10
}}
"""

def verify_claim(claim: str, search_results: list) -> dict:
    """Sends claim and search results to the AI to get a verdict and score."""
    print(f"⚖️  Judging claim: '{claim}'...")
    
    # Format search results into a readable string for the AI
    results_text = "\n".join([f"- {r['title']} ({r['date']}): {r['snippet']}" for r in search_results])
    
    try:
        response = client.chat.completions.create(
            model=STRONG_MODEL,
            messages=[
                {"role": "system", "content": "You are a strict fact-checking assistant that outputs ONLY valid JSON."},
                {"role": "user", "content": VERIFICATION_PROMPT.format(claim=claim, search_results=results_text)}
            ],
            temperature=0.0, # Zero temperature for strict, deterministic judging
            response_format={"type": "json_object"}
        )
        
        raw_output = response.choices[0].message.content
        raw_output = raw_output.replace("```json", "").replace("```", "").strip()
        
        return json.loads(raw_output)
            
    except Exception as e:
        print(f"❌ Error verifying claim: {e}")
        return {"status": "Cannot verify", "reason": "AI error", "freshness_score": 50}

# 4. Test it out!
if __name__ == "__main__":
    # Simulating the output from our extractor and searcher
    sample_claim = "Twitter is currently led by CEO Jack Dorsey"
    sample_results = [
        {
            "title": "Jack Dorsey Steps Down as Twitter CEO",
            "url": "https://example.com/dorsey-steps-down",
            "date": "2021-11-29",
            "snippet": "SAN FRANCISCO, Nov. 29, 2021 -- Twitter, Inc. announced today that Jack Dorsey has stepped down as CEO..."
        },
        {
            "title": "Elon Musk completes acquisition of Twitter",
            "url": "https://example.com/musk-twitter",
            "date": "2022-10-27",
            "snippet": "Elon Musk has officially completed his $44 billion acquisition of Twitter, becoming the new owner and effectively the CEO."
        }
    ]
    
    print("--- TESTING VERIFIER ---")
    verdict = verify_claim(sample_claim, sample_results)
    
    print("\n✅ VERDICT:")
    print(f"Status: {verdict.get('status')}")
    print(f"Score: {verdict.get('freshness_score')}/100")
    print(f"Reason: {verdict.get('reason')}")