from gmail_client import get_gmail_service, get_unread_emails
from agent import analyze_sales_email
from guardrails import validate_draft


print("=" * 70)
print("              AI SALES INBOX AGENT")
print("=" * 70)

print("\nConnecting to Gmail...")

service = get_gmail_service()

print("Gmail connected successfully! ✅")

emails = get_unread_emails(service, max_results=10)

print(f"\nUnread emails found: {len(emails)}")


if not emails:
    print("\nNo unread emails found.")
    print("Send a test email and run the script again.")
    exit()


for number, email in enumerate(emails, start=1):

    print("\n")
    print("=" * 70)
    print(f"                    EMAIL {number}")
    print("=" * 70)

    print("\nFROM:")
    print(email["sender"])

    print("\nSUBJECT:")
    print(email["subject"])

    print("\nBODY:")
    print(email["body"][:1000])

    print("\n" + "-" * 70)
    print("Analyzing email with Groq AI...")
    print("-" * 70)

    try:
        analysis = analyze_sales_email(email)

    except Exception as error:
        print("\n❌ AI analysis failed.")
        print("Error:", error)
        continue


    # ---------------------------------------------------------
    # AI ANALYSIS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("AI SALES ANALYSIS")
    print("=" * 70)

    print("\nLead Name:")
    print(analysis["lead_name"])

    print("\nCompany:")
    print(analysis["company"])

    print("\nIntent:")
    print(analysis["intent"])

    print("\nUrgency:")
    print(analysis["urgency"])

    print("\nRequirements:")
    for requirement in analysis["requirements"]:
        print(f"- {requirement}")

    print("\nTimeline:")
    print(analysis["timeline"])

    print("\nRecommended Action:")
    print(analysis["recommended_action"])

    print("\nReasoning:")
    print(analysis["reasoning"])


    # ---------------------------------------------------------
    # GUARDRAILS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("GUARDRAIL CHECK")
    print("=" * 70)

    problems = validate_draft(
        analysis["draft_reply"]
    )

    if problems:

        print("\n⚠️ HUMAN REVIEW REQUIRED")

        for problem in problems:
            print(f"- {problem}")

    else:

        print("\n✓ No guardrail violations detected.")


    # ---------------------------------------------------------
    # DRAFT REPLY
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("DRAFT REPLY")
    print("=" * 70)

    print("\nSubject:")
    print(analysis["draft_subject"])

    print("\nReply:")
    print(analysis["draft_reply"])


    # ---------------------------------------------------------
    # HUMAN REVIEW
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("HUMAN REVIEW")
    print("=" * 70)

    print("\nAI recommendation:")
    print(analysis["recommended_action"])

    print(
        "\nApprove this draft? "
        "[approve/edit/reject/skip]: "
    )

    decision = input("> ").strip().lower()


    if decision == "approve":

        print("\n✓ Draft approved for sending.")
        print("⚠ Email sending is disabled in this MVP.")

    elif decision == "edit":

        print("\n→ Human editing required.")
        print("The draft should be edited before sending.")

    elif decision == "reject":

        print("\n✗ Draft rejected.")

    elif decision == "skip":

        print("\n→ Review skipped.")

    else:

        print("\n⚠ Invalid decision. Moving to next email.")


    print("\n")


# -------------------------------------------------------------
# FINISHED
# -------------------------------------------------------------

print("=" * 70)
print("                 PROCESSING COMPLETE")
print("=" * 70)

print("\nAll unread emails have been processed.")
print("No emails were automatically sent.")
print("Human approval is required before any customer-facing action.")
