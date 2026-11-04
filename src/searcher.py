import os
from dotenv import load_dotenv
from tavily import TavilyClient

# 1. Load environment variables
load_dotenv()

# 2. Initialize Tavily Client
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY or TAVILY_API_KEY == "paste_your_tavily_key_here":
    raise ValueError("❌ Please add your real Tavily API key to the .env file!")

client = TavilyClient(api_key=TAVILY_API_KEY)

def search_claim(claim: str) -> list:
    """Searches the live web for a specific claim using Tavily."""
    print(f"🔎 Searching live web for: '{claim}'...")
    try:
        # Search Tavily for recent, factual information
        response = client.search(
            query=claim,
            search_depth="advanced", # Gets better, more detailed results
            max_results=3,           # We only need top 3 sources
            include_answer=True      # Gets a quick AI summary from Tavily
        )
        
        # Extract relevant info from the results
        results = []
        for res in response.get("results", []):
            results.append({
                "title": res.get("title"),
                "url": res.get("url"),
                "snippet": res.get("content"),
                "date": res.get("published_date", "Unknown")
            })
        return results
        
    except Exception as e:
        print(f"❌ Error searching Tavily: {e}")
        return []

# 3. Test it out!
if __name__ == "__main__":
    # A sample stale claim
    sample_claim = "Twitter is currently led by CEO Jack Dorsey"
    
    print("--- TESTING TAVILY SEARCH ---")
    results = search_claim(sample_claim)
    
    print(f"\n✅ Found {len(results)} results:")
    for i, res in enumerate(results, 1):
        print(f"\n{i}. {res['title']}")
        print(f"   URL: {res['url']}")
        print(f"   Date: {res['date']}")
        print(f"   Snippet: {res['snippet'][:100]}...") # Print first 100 chars