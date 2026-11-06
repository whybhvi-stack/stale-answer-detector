import os
from datetime import date
from urllib.parse import urlparse
from dotenv import load_dotenv
from tavily import TavilyClient
from llm import ask_json

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Sites we do not trust as evidence (add more any time)
BAD_HINTS = ["staging.", "businessofapps.com", "liquidweb.com"]

SYSTEM = """You check if a claim is still true using search results.
Today's date is {today}.
Each source has a date. Prefer the NEWEST sources.
Prefer official sites, documentation, and well-known news or reference sites.
Never use your own memory, only the sources.
Rules for the verdict:
- still_true: a recent source confirms the claim.
- outdated: a recent source shows the claim is no longer true.
- cannot_verify: sources are old, unclear, or do not answer the claim.
For correct_info, write the new fact only if the sources clearly state it.
In supporting_indexes, list the numbers of ALL sources that state that new fact.
If a company or product was renamed, mention the new name.
Return ONLY JSON:
{{"verdict": "still_true|outdated|cannot_verify", "reason": "one short sentence",
 "correct_info": "the up-to-date fact, or empty", "supporting_indexes": [0],
 "best_source_index": 0}}"""

def domain_of(url):
    return urlparse(url).netloc.replace("www.", "")

def verify_claim(claim_obj):
    kwargs = {"max_results": 8, "time_range": "year"}
    if claim_obj.get("type") in ("leadership", "stat"):
        kwargs["topic"] = "news"
    search = tavily.search(claim_obj["search_query"], **kwargs)
    results = [r for r in search["results"]
               if not any(h in r["url"] for h in BAD_HINTS)][:5]
    if not results:
        return {"verdict": "cannot_verify", "reason": "No good recent sources found.",
                "correct_info": "", "best_source_index": 0}, []

    sources_text = "\n".join(
        f"[{i}] {r['title']} ({r['url']}) | date: {r.get('published_date') or 'unknown'} | {r['content'][:400]}"
        for i, r in enumerate(results)
    )
    prompt = f"Claim: {claim_obj['claim']}\n\nSearch results:\n{sources_text}"
    system = SYSTEM.format(today=date.today().isoformat())
    verdict = ask_json(os.getenv("STRONG_MODEL"), system, prompt)

    # Our own safety check: a correction needs 2 different websites
    if verdict.get("correct_info"):
        idxs = [i for i in verdict.get("supporting_indexes", [])
                if isinstance(i, int) and i < len(results)]
        domains = {domain_of(results[i]["url"]) for i in idxs}
        if len(domains) < 2:
            verdict["correct_info"] = ""
            verdict["reason"] += " (The current answer could not be confirmed by two independent sources.)"
        if verdict.get("verdict") == "outdated" and not verdict.get("correct_info"):
         verdict["reason"] = ("Sources suggest this claim is out of date, but the current answer "
                             "could not be confirmed by two independent sources.")  
    return verdict, results