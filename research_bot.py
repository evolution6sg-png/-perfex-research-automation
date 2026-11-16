import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from openai import OpenAI

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PERFEX RESEARCH BOT
# Bi-weekly aluminium radiator
# market intelligence report
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Configuration
RECIPIENT_EMAIL = "darren.phua@perfex.com.sg"
SENDER_EMAIL = os.environ["GMAIL_SENDER"]
GMAIL_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Today's date
today = datetime.date.today()
next_report = today + datetime.timedelta(days=14)
report_period_start = today - datetime.timedelta(days=14)

# Format dates
today_str = today.strftime("%d %B %Y")
next_str = next_report.strftime("%d %B %Y")
period_str = report_period_start.strftime("%d %B %Y")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESEARCH PROMPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

research_prompt = f"""
PERFEX INTERNATIONAL — BI-WEEKLY
ALUMINIUM RADIATOR MARKET AND
COMPETITOR INTELLIGENCE REPORT

Report date: {today_str}
Report period: {period_str} to {today_str}
Next report due: {next_str}
Prepared for: Darren Phua
Head of Sales, Perfex International
darren.phua@perfex.com.sg

BACKGROUND CONTEXT:
Perfex International Pte Ltd is a
Singapore-based manufacturer of
industrial cooling systems and
radiators, primarily copper-brass,
serving genset OEMs and EPCs across
Southeast Asia.

Perfex is running a 12-month pilot
for aluminium brazed radiators targeting:
- Genset OEMs: Rehlko, Generac,
  Cummins/IEA, Perkins/COG
- Data centre standby power
- Markets: Singapore, Malaysia (Johor),
  Indonesia, Philippines, Vietnam,
  Thailand, Taiwan

Key strategic facts:
- Competitor offering aluminium radiators
  30% below Perfex copper-brass pricing
- Copper at 4.6x aluminium cost
  (LME baseline 10 Nov 2026)
- Johor data centre pipeline:
  1,110 MW live, 602 MW under
  construction, 2,486 MW planned
- Cost of losing a sale: S$3,590/unit
- Cost of cannibalisation: S$210/unit

Search the web for developments in
the past 14 days on ALL sections below.
Produce a complete structured report.

SECTION 1 - ALUMINIUM MARKET NEWS
Search for new product launches,
technology developments, OEM approvals,
aluminium price movements, supply chain
developments, new coastal coating
technologies.

SECTION 2 - COMPETITOR INTELLIGENCE

2A - Track these competitors:
TIER 1: Modine, AKG/AKG India,
Wabtec/L&M Radiator, IEA (Cummins),
COG (Perkins)
TIER 2: Chinese aluminium radiator
manufacturers exporting to SEA
TIER 3: Regional SEA competitors

2B - Pricing Intelligence:
Any reported pricing for aluminium
genset radiators in SEA, tender results,
price changes, Chinese supplier pricing.

2C - New Product Launches:
New aluminium radiator models for
gensets, trade show announcements,
new specifications, tropical/coastal
products, engines above 2MW.

2D - Market Share Shifts:
OEM supplier changes, new distributor
appointments, major contract wins/losses
in SG/MY/ID/PH/VN/TH.

2E - Competitor Strategic Moves:
SEA expansion, new manufacturing
capacity, mergers/acquisitions,
marketing campaigns, certifications.

2F - Competitor Scorecard:
Rate each competitor threat:
Modine, AKG India, Wabtec/L&M,
IEA Cummins, COG Perkins,
Chinese manufacturers, Regional.
Use RED/AMBER/GREEN and show
change vs last fortnight.

SECTION 3 - GENSET OEM DEVELOPMENTS
News about: Rehlko, Generac, Cummins,
Caterpillar, MTU, new OEMs in SEA.

SECTION 4 - DATA CENTRE DEVELOPMENTS
New data centres in SG/MY/ID/PH/VN/TH/TW,
operators: Microsoft, Equinix, Vantage,
Google, AWS, Meta, ByteDance, GDS,
ST Telemedia. HVO adoption news.

SECTION 5 - RAW MATERIAL PRICES
Current LME: Aluminium $/tonne,
Copper $/tonne, Cu/Al ratio.
Baseline: Cu $13,876/t, Al $3,031/t,
ratio 4.6x (10 Nov 2026).
Show change vs baseline.

SECTION 6 - REGULATORY DEVELOPMENTS
New regulations in SG/MY/ID/PH/VN
affecting diesel gensets or cooling.
HVO policies, efficiency standards.

SECTION 7 - MANAGEMENT SUMMARY
Executive summary (5 bullets max).
RED immediate actions this week.
AMBER monitor next fortnight.
GREEN positive developments.
Competitive position: Increasing/
Stable/Decreasing threat.
Biggest threat this fortnight.
Biggest opportunity this fortnight.
Pilot programme relevance.
Action register: Action/Owner/Date/
Expected Outcome.

Format everything clearly with
headers, bullet points and
RED/AMBER/GREEN flags throughout.
Write for Head of Sales reading
on screen. Be concise and commercial.
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CALL OPENAI API
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_report():
    client = OpenAI(api_key=OPENAI_API_KEY)

    print("Generating Perfex research report...")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """You are a commercial intelligence
                researcher for Perfex International Pte Ltd,
                a Singapore industrial cooling systems company.
                Search the web thoroughly and produce detailed,
                accurate market intelligence reports.
                Always use RED/AMBER/GREEN priority flags.
                Write in concise executive language."""
            },
            {
                "role": "user",
                "content": research_prompt
            }
        ],
        max_tokens=4000,
        temperature=0.3
    )

    report = response.choices[0].message.content
    print("Report generated successfully!")
    return report

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SEND EMAIL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def send_email(report_content):
    subject = (
        f"Perfex Aluminium Radiator Intelligence "
        f"— {today_str}"
    )

    # Create email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    # Email body
    email_body = f"""
PERFEX ALUMINIUM RADIATOR
BI-WEEKLY INTELLIGENCE REPORT
{today_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{report_content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated automatically by
Perfex Research Bot
Next report: {next_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """

    msg.attach(MIMEText(email_body, "plain"))

    # Send via Gmail
    print(f"Sending email to {RECIPIENT_EMAIL}...")

    with smtplib.SMTP_SSL(
        "smtp.gmail.com", 465
    ) as server:
        server.login(SENDER_EMAIL, GMAIL_PASSWORD)
        server.sendmail(
            SENDER_EMAIL,
            RECIPIENT_EMAIL,
            msg.as_string()
        )

    print("Email sent successfully!")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN EXECUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    print("Starting Perfex Research Bot...")
    print(f"Report date: {today_str}")
    print(f"Recipient: {RECIPIENT_EMAIL}")

    # Generate report
    report = generate_report()

    # Send email
    send_email(report)

    print("Perfex Research Bot completed!")
