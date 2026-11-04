import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

result = client.search("OpenAI API pricing gpt-4o", max_results=3)
for r in result["results"]:
    print(r["title"])
    print(r["url"])
    print(r["content"][:150])
    print("---")