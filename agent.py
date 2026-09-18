import os
import json
import re

from groq import Groq
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_json(text):
    """
    Extract JSON from the model response.
    Handles cases where the model wraps JSON in ```json ... ```
    """

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # Find JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            f"Model did not return valid JSON.\n\n"
            f"Model response:\n{text}"
        )

    json_text = text[start:end + 1]

    return json.loads(json_text)


def analyze_sales_email(email):
    """
    Analyze one incoming email and return structured sales intelligence.
    """

    prompt = f"""
You are an AI Sales Inbox Agent.

Your job is to analyze an incoming email and determine whether it is a
real customer/lead inquiry or a non-actionable email.

IMPORTANT NAME RULE:

The Gmail "From" field may belong to the mailbox owner or the person
sending the test email, and therefore MUST NOT automatically be treated
as the lead's name.

When identifying the lead name:

1. First look for a person's name in the email body.
2. Pay special attention to signatures such as:
   "Thanks, Ahmed"
   "Best, Michael"
   "Regards, Sarah"
3. If the body clearly identifies the sender, use that name.
4. If the body does not contain a reliable name, use the Gmail From name
   only if it is clearly appropriate.
5. If there is still uncertainty, return an empty string.
6. Never invent a person's name.

IMPORTANT EMAIL TYPE RULE:

First determine whether the email is:

- a genuine customer/lead inquiry
OR
- a newsletter
- marketing email
- promotional email
- product announcement
- subscription notification
- automated notification
- unrelated/non-customer email

If the email is a newsletter, marketing email, product announcement,
promotional email, notification, or other non-customer inquiry:

- set recommended_action to NO_ACTION
- set draft_subject to ""
- set draft_reply to ""
- do NOT generate a customer reply
- explain why in the reasoning field

For genuine customer/lead inquiries, analyze the sales opportunity and
prepare a concise draft reply.

Return ONLY a JSON object.

The JSON must contain EXACTLY these fields:

{{
  "lead_name": "",
  "company": "",
  "intent": "",
  "urgency": "low",
  "requirements": [],
  "timeline": "",
  "recommended_action": "",
  "reasoning": "",
  "draft_subject": "",
  "draft_reply": "",
  "human_review_required": true
}}

IMPORTANT RULES:

1. Use ONLY information explicitly provided in the email.

2. Do not invent or assume business facts.

3. Never claim previous experience, customers, results, case studies,
   expertise, services, or capabilities unless explicitly provided.

4. Never invent meeting dates, times, duration, availability,
   calendar links, or contact details.

5. Never invent pricing, discounts, guarantees, commitments,
   or delivery timelines.

6. If important information is missing, ask the customer for it instead
   of guessing.

7. The reply must be professional and personalized.

8. human_review_required must ALWAYS be true.

9. Recommended actions for genuine customer inquiries can only be:

   BOOK_CALL
   REQUEST_INFORMATION
   SEND_INFORMATION
   FOLLOW_UP_LATER
   HUMAN_REVIEW
   NO_ACTION

10. Use BOOK_CALL when the customer explicitly asks to schedule a call
    or meeting.

11. Use REQUEST_INFORMATION when the customer needs information that
    is not currently available from the email context.

12. Use SEND_INFORMATION when the customer is requesting information
    that can be directly addressed from the information provided.

13. Use FOLLOW_UP_LATER only when the email represents a genuine
    customer/lead conversation that should be followed up later.

14. Use HUMAN_REVIEW when the message is potentially important but the
    correct action cannot be safely determined automatically.

15. Use NO_ACTION for newsletters, marketing emails, advertisements,
    product announcements, subscription notifications, automated
    notifications, and unrelated emails.

16. For NO_ACTION emails:
    - draft_subject MUST be ""
    - draft_reply MUST be ""

17. For a genuine customer email, the draft reply must NOT contain
    placeholders such as:
    [Your Name]
    [Company]
    [Name]
    [Your Company]

18. Do not use generic placeholders of any kind.

19. Do not sign the email with a name unless the sender/reply identity
    is explicitly provided in the available information.

20. If a call is appropriate, simply ask the customer to suggest
    a convenient time.

21. Do not claim that a specific time is available.

22. Do not automatically send or imply that the email has been sent.

23. Do not modify the customer's original email.

24. Return valid JSON only.

EMAIL INFORMATION:

Gmail From:
{email["sender"]}

Subject:
{email["subject"]}

Email Body:
{email["body"]}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful sales operations assistant. "
                    "You prioritize factual accuracy, safety, and "
                    "human review over making assumptions."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content

    print("\nRaw Groq response:")
    print(content)

    analysis = extract_json(content)

    # ---------------------------------------------------------
    # Safety normalization for NO_ACTION
    # ---------------------------------------------------------
    if analysis.get("recommended_action") == "NO_ACTION":
        analysis["draft_subject"] = ""
        analysis["draft_reply"] = ""

    return analysis