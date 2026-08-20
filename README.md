# Morning Market Briefing Bot

Automated daily market briefing generator, powered by Claude. Every morning it researches current market conditions using live web search, writes a full analyst-style briefing in plain English, and emails it straight to your inbox — no manual work required.

## Why this exists

Most market newsletters are either too generic to be useful or too jargon-heavy to be readable without a finance background. This project uses Claude with real-time web search to produce a genuinely researched briefing every day — specific tickers, real numbers, clear calls — written so anyone can actually understand what's happening and why it matters.

## What you get

A formatted HTML email covering:

- **Market Pulse** — overbought/oversold signals, fear vs. greed, VIX, put/call ratio, and what it all means
- **Market Overview** — the macro story and news driving the day
- **Ticker Breakdown** — 6–8 names with what's happening, why it matters, and a clear BUY / HOLD / AVOID call
- **Unusual Volume / Options Activity** — where positioning looks abnormal and what it signals
- **Earnings** — last night's reports plus today's key names to watch
- **Sector Watch** — AI, tech, energy, financials, cyclicals, defensives, gold and silver
- **Wildcard** — one under-the-radar idea or macro theme worth knowing

## How it works

Claude is given web search access (capped at 5 queries) and a tightly specced system prompt covering both content structure and exact HTML/CSS styling, so the output is current, grounded in real data, and consistently formatted with zero manual editing — custom fonts, ticker cards, and color-coded rating badges included.

## Setup

1. Clone the repo and install dependencies:
```bash
   pip install anthropic python-dotenv
```
2. Create a `.env` file in the project root (not committed) with:   Use a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your real Gmail password.
3. Run it:
```bash
   python morning_briefing.py
```

## What I learned building this

- **Prompt engineering for structured output** — getting an LLM to reliably return clean, consistently-styled HTML instead of freeform text, on the first try, every time.
- **Wiring an LLM into a real pipeline** — search → generation → formatted delivery, instead of just chatting with a model. Same pattern that scales to a lot of other automation use cases.

## Possible next steps

- Schedule with cron or GitHub Actions to run automatically every morning
- Add retry/error handling on email send failures
- Let recipients customize which tickers/sectors they care about
