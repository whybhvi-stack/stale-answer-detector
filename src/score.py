from urllib.parse import urlparse

TRUSTED_HINTS = [
    "docs.", ".gov", "github.com", "openai.com", "anthropic.com",
    "wikipedia.org", "reuters.com", "bbc.com", "python.org", "aljazeera.com",
]

def freshness_score(verdict, source_url):
    base = {"still_true": 75, "cannot_verify": 40, "outdated": 10}.get(verdict["verdict"], 40)
    domain = urlparse(source_url).netloc if source_url else ""
    if any(h in domain or h in source_url for h in TRUSTED_HINTS):
        bonus = 20
    elif "staging" in domain or "test" in domain:
        bonus = -15
    else:
        bonus = 5
    return max(0, min(100, base + bonus))

def color(score):
    if score >= 70:
        return "green"
    if score >= 40:
        return "orange"
    return "red"