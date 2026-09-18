from gmail_client import get_gmail_service, get_unread_emails


print("Connecting to Gmail...")

service = get_gmail_service()

print("Gmail connected successfully! ✅")

emails = get_unread_emails(service)

print(f"\nUnread emails found: {len(emails)}")

for email in emails:

    print("\n" + "=" * 60)

    print("FROM:")
    print(email["sender"])

    print("\nSUBJECT:")
    print(email["subject"])

    print("\nBODY:")
    print(email["body"][:500])