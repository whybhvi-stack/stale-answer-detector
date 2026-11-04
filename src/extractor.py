import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables from .env file
load_dotenv()

# 2. Configure the OpenAI client to talk to your LOCAL Bifrost server
client = OpenAI(
    base_url=os.getenv("BIFROST_BASE_URL"),
        api_key=os.getenv("OPENROUTER_API_KEY") # Bifrost doesn't strictly need a real key for local routing
)

CHEAP_MODEL = os.getenv("CHEAP_MODEL", "openai/gpt-4o-mini")

# 3. The Prompt: Explicitly ask for a JSON OBJECT with a "claims" array
EXTRACTION_PROMPT = """
You are a fact-checking assistant. Analyze the following text and extract every distinct factual claim.
For each claim, determine if it is "time-sensitive" (e.g., mentions prices, dates, software versions, current CEOs, laws, or statistics that could change).

Return ONLY a valid JSON object with a single key "claims" containing an array of objects.
Each object in the array must have:
- "claim": (string) The exact factual claim.
- "is_time_sensitive": (boolean) true if it could be outdated, false if it's a permanent fact.

Example output:
{{
  "claims": [
    {{"claim": "The API costs $0.002 per 1k tokens.", "is_time_sensitive": true}},
    {{"claim": "Python is a programming language.", "is_time_sensitive": false}}
  ]
}}

Text to analyze:
{text}
"""

def extract_claims(text: str) -> list:
    """Sends text to Bifrost and returns a list of extracted claims."""
    print(f"🔍 Extracting claims using model: {CHEAP_MODEL}...")
    
    try:
        response = client.chat.completions.create(
            model=CHEAP_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs ONLY valid JSON."},
                {"role": "user", "content": EXTRACTION_PROMPT.format(text=text)}
            ],
            temperature=0.1, # Low temperature for consistent, factual extraction
            response_format={"type": "json_object"} # Forces OpenAI/Bifrost to return valid JSON {}
        )
        
        # Parse the JSON string from the AI into a Python dictionary
        raw_output = response.choices[0].message.content
        
        # Clean up markdown code blocks if the model adds them anyway
        raw_output = raw_output.replace("```json", "").replace("```", "").strip()
        
        claims_data = json.loads(raw_output)
        
        # Safely extract the "claims" list from the dictionary
        return claims_data.get("claims", [])
            
    except Exception as e:
        print(f"❌ Error extracting claims: {e}")
        print(f"Raw output was: {raw_output if 'raw_output' in locals() else 'N/A'}")
        return []

# 4. Test it out!
if __name__ == "__main__":
    # A sample "stale" AI answer (e.g., old Twitter CEO and old API pricing)
    sample_ai_answer = """
    Twitter is currently led by CEO Jack Dorsey, who returned to the company in 2015. 
    Also, the OpenAI GPT-4 API currently costs $0.03 per 1,000 input tokens. 
    Water boils at 100 degrees Celsius at sea level.
    """
    
    print("--- SAMPLE AI ANSWER ---")
    print(sample_ai_answer)
    print("------------------------\n")
    
    claims = extract_claims(sample_ai_answer)
    
    print("\n✅ EXTRACTED CLAIMS:")
    for i, item in enumerate(claims, 1):
        sensitive_flag = "⚠️ TIME-SENSITIVE" if item.get("is_time_sensitive") else "✅ STATIC"
        print(f"{i}. [{sensitive_flag}] {item.get('claim')}")