# Test results

Tested on 6 Nov 2026 with the Streamlit app. "Reality" was checked by hand on the web the same day.
Run 1 is the first version of the app. Run 2 is after three small fixes (leaked wrong replacement fact,
missed claim, blank screen). Answers 2, 3 and 5 were not re-run after the fixes.

| # | Answer tested | Run 1 (before fixes) | Run 2 (after fixes) | Reality (checked by hand) |
|---|---|---|---|---|
| 1 | GPT-4 is OpenAI's most advanced model, and the API costs $30 per million input tokens. | Only the price was checked: still_true (80/100). The "most advanced model" claim was missed. | "Most advanced model": outdated (15/100), says the current answer could not be confirmed. Price: cannot_verify (45/100). | The price is still $30 per 1M input tokens, but GPT-4 is a legacy model, so the answer is stale. |
| 2 | The latest version of Node.js is 18, and it is the current LTS release. | outdated (15/100). The replacement shown (24.x) was itself old. | Not re-run. | Node.js 26.13.0 became LTS on 28 Oct 2026. Node 18 is old. |
| 3 | The EU AI Act is still only a proposal and has not become law. | outdated (15/100): adopted and in force. | Not re-run. | In force since 1 Aug 2024. A July 2026 amendment delays some high-risk deadlines. |
| 4 | The latest iPhone is the iPhone 13. | outdated (15/100), but showed "iPhone 17 Pro" as the replacement, which is stale. | outdated (15/100). No wrong replacement shown; says the current answer could not be confirmed. | iPhone 18 Pro and Pro Max were presented in Sept 2026 (confirm on apple.com). |
| 5 | Google's CEO is Sundar Pichai. | cannot_verify (45/100). | Not re-run. | Sources list Pichai as CEO of Google and Alphabet, but they were undated, so there was no recent confirmation. |
| 6 | The capital of France is Paris. | Nothing shown on screen. | "No time-sensitive claims found, so nothing in this answer can go stale." | Nothing in this sentence can go stale. |

## Summary

- Stale answers flagged: 4 of 4 (answers 2 and 3 in Run 1, answers 1 and 4 in Run 2).
- False alarms: 0.
- Wrong replacement facts shown: 2 in Run 1 (answers 2 and 4). 0 after the fix for answer 4. Answer 2 was not re-run.

## Known limitations

- When two independent sources do not confirm the new fact, the app says so instead of guessing.
  This is on purpose, but it means some answers end as "outdated, current answer not confirmed".
- In Run 2 the GPT-4 price claim moved from still_true to cannot_verify. The extracted claim
  did not include the product name "GPT-4", which probably made the search too vague.
- "Source date" often shows "unknown", because the search results do not always include a date.
- Only 6 answers were tested, so these numbers show the idea works but are not a full benchmark.

## Sources used for checking

- GPT-4 pricing: https://www.developersdigest.tech/models/gpt-4
- GPT-4 is a legacy model: https://www.cloudzero.com/blog/gpt-4-api-cost
- Node.js 26.13.0 LTS: https://nodejs.org/en/blog/release/v26.13.0
- EU AI Act and the 2026 amendment: https://cms.law/en/gbr/publication/the-eu-s-digital-omnibus-streamlined-ai-act-compliance-rules-are-now-in-force
- iPhone 18 Pro launch: https://www.lte-anbieter.info/smartphones/apple-iphone-18-pro-pro-max
- Sundar Pichai: https://www.britannica.com/money/Sundar-Pichai 