import anthropic
import smtplib
import os
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_market_briefing():
    today = date.today().strftime("%B %d, %Y")

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=16000,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search"
            }],
            system="""You are a financial analyst delivering a morning market briefing to a non-professional investor. 
        Be specific — real tickers, real numbers, real context. No fluff. No disclaimers.
        Use clear, simple language — explain why things matter in plain English, not Wall Street jargon.
        Do not narrate your process or thinking. Do not write anything before the HTML. Start your response with <!DOCTYPE html> immediately.
        Limit yourself to 5 web searches maximum.
        Output only clean HTML. No markdown. No code fences. Just the HTML.""",
            messages=[{
                "role": "user",
                "content": f""" Today is {today}, Generate my morning market briefing as a formatted HTML email.

    Use this exact structure:

1. MARKET PULSE — overall market health check. Cover: is the market overbought or oversold (RSI levels), fear vs greed index, VIX level and what it signals, put/call ratio, any divergences worth watching. Write this in plain English — tell her what it all means, not just the numbers.
2. MARKET OVERVIEW — pre-market sentiment, key macro news driving the day, general large events. 3-4 paragraphs minimum.
3. TICKER BREAKDOWN — 6-8 tickers worth watching. For each: what's happening (2-3 sentences), why it matters (2-3 sentences), the play (2-3 sentences), and a clear BUY / HOLD / AVOID rating with one sentence explaining why.
4. UNUSUAL VOLUME / OPTIONS ACTIVITY — 3-4 tickers with abnormal activity, explain what the positioning signals and why it matters.
5. EARNINGS — last night's reports with key numbers, plus 3-4 ones to watch today with analyst expectations.
6. SECTOR WATCH — what's hot and what's not across AI, tech, energy, financial services, cyclical, defensive. Also cover gold and silver — price levels, trend, and whether they're worth watching. 2-3 sentences per sector.
7. WILDCARD — one under-the-radar idea or macro theme worth knowing. 2-3 paragraphs.

    HTML formatting requirements:
    - In the <head>, import Google Fonts: Playfair Display (headers) and Nunito (body)
    - Body font: Nunito, 16px, line-height 1.8, color #333333
    - Section headers: Playfair Display, 22px, color #1a1a2e
    - Wrapper: max-width 700px, margin 0 auto, padding 40px 20px
    - Each ticker in section 2 gets its own card: background #f9f9f9, border 1px solid #e0e0e0, border-radius 8px, padding 16px, margin-bottom 12px
    - Section dividers: a simple <hr> with border-top 1px solid #e0e0e0, margin 32px 0
    - Add extra padding between sections: margin 48px 0 on each section
    - Add margin-bottom 24px between paragraphs inside each section
    - Do not use italic text anywhere
    - Each section must have a clear bold header with a colored left border: border-left 4px solid #1a1a2e, padding-left 12px
    - Each ticker card must include: ticker symbol in large bold text (20px), company name below it in gray (#666), then what's happening, why it matters, the play, and BUY/HOLD/AVOID as a colored badge (BUY = green #2d6a4f, HOLD = orange #e07b00, AVOID = red #c0392b)
    - BUY/HOLD/AVOID must be displayed as a pill badge: border-radius 20px, padding 4px 12px, color white, font-weight bold
    - Top of email: large greeting — Good Morning. Here's your briefing for {today}.
    - Output ONLY the HTML. Nothing else."""
            }]       
        )
    except anthropic.APIStatusError as e:
        print(f"API error: {e}")
        return None

    briefing = ""
    for block in response.content:
        if block.type == "text":
            briefing += block.text

    return briefing 

def send_email(briefing):
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")
    recipients = [os.getenv("RECIPIENT_EMAIL"), os.getenv("RECIPIENT_EMAIL_2")]
    today = date.today().strftime("%B %d, %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Morning Market Briefing — {today}"
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    msg.attach(MIMEText(briefing, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())

    print("Email sent.")

if __name__ == "__main__":
    print("Fetching market briefing...")
    briefing = get_market_briefing()
    if briefing is None:
        print("Failed to get briefing. Exiting.")
    else:
        print("Sending email...")
        send_email(briefing)
        print("Done.")