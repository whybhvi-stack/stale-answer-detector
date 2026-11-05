import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from extractor import extract_claims
from searcher import search_claim
from verify import verify_claim

def run_stale_answer_detector(ai_answer):
    print("=" * 60)
    print("STALE-ANSWER DETECTOR - Starting Analysis")
    print("=" * 60)
    
    print("\nSTEP 1: Extracting claims from AI answer...")
    claims = extract_claims(ai_answer)
    
    if not claims:
        print("No claims extracted. Exiting.")
        return
    
    print(f"Found {len(claims)} claims")
    
    results = []
    for i, item in enumerate(claims, 1):
        claim_text = item.get("claim")
        is_sensitive = item.get("is_time_sensitive")
        
        print(f"\n{'='*60}")
        print(f"CLAIM {i}: {claim_text}")
        print(f"Type: {'TIME-SENSITIVE' if is_sensitive else 'STATIC'}")
        
        if not is_sensitive:
            results.append({
                "claim": claim_text,
                "status": "Still true",
                "freshness_score": 100,
                "reason": "Permanent fact (not time-sensitive)",
                "sources": []
            })
            continue
        
        search_results = search_claim(claim_text)
        
        if not search_results:
            results.append({
                "claim": claim_text,
                "status": "Cannot verify",
                "freshness_score": 50,
                "reason": "No search results found",
                "sources": []
            })
            continue
        
        verdict = verify_claim(claim_text, search_results)
        
        results.append({
            "claim": claim_text,
            "status": verdict.get("status"),
            "freshness_score": verdict.get("freshness_score"),
            "reason": verdict.get("reason"),
            "sources": search_results
        })
    
    print("\n" + "=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    
    total_score = sum(r["freshness_score"] for r in results)
    avg_score = total_score / len(results) if results else 0
    
    print(f"\nOverall Freshness Score: {avg_score:.1f}/100")
    print(f"Total Claims: {len(results)}")
    
    print("\n--- DETAILED RESULTS ---")
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['claim']}")
        print(f"   Status: {r['status']}")
        print(f"   Score: {r['freshness_score']}/100")
        print(f"   Reason: {r['reason']}")
        if r['sources']:
            print(f"   Source: {r['sources'][0]['url']}")
    
    return results

if __name__ == "__main__":
    sample_ai_answer = "Twitter is currently led by CEO Jack Dorsey. The OpenAI GPT-4 API currently costs $0.03 per 1,000 input tokens. Water boils at 100 degrees Celsius at sea level."
    run_stale_answer_detector(sample_ai_answer)