from claims import extract_claims
from verify import verify_claim
from score import freshness_score, color

def check_answer(answer):
    report = []
    for c in extract_claims(answer):
        verdict, results = verify_claim(c)
        idx = verdict.get("best_source_index", 0)
        if results and isinstance(idx, int) and idx < len(results):
            url = results[idx]["url"]
            source_date = results[idx].get("published_date") or "unknown"
        else:
            url, source_date = "", "unknown"
        score = freshness_score(verdict, url)
        report.append({
            "claim": c["claim"],
            "type": c["type"],
            "verdict": verdict["verdict"],
            "reason": verdict["reason"],
            "correct_info": verdict.get("correct_info", ""),
            "source": url,
            "source_date": source_date,
            "score": score,
            "color": color(score),
        })
    return report

if __name__ == "__main__":
    test = "Python 3.9 is the latest Python version. The CEO of Twitter is Jack Dorsey."
    for r in check_answer(test):
        print(r)
        print()