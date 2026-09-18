import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    creds = None

    try:
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )
    except Exception:
        pass

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def extract_body(payload):
    """
    Extract plain-text body from a Gmail message.
    """

    if "parts" in payload:
        for part in payload["parts"]:

            if part["mimeType"] == "text/plain":

                data = part["body"].get("data")

                if data:
                    return base64.urlsafe_b64decode(
                        data
                    ).decode("utf-8")

    data = payload["body"].get("data")

    if data:
        return base64.urlsafe_b64decode(
            data
        ).decode("utf-8")

    return ""


def get_unread_emails(service, max_results=5):
    """
    Get unread emails from the Gmail inbox.
    """

    response = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results
    ).execute()

    messages = response.get("messages", [])

    emails = []

    for message in messages:

        data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        headers = data["payload"].get("headers", [])

        subject = ""
        sender = ""

        for header in headers:

            name = header["name"].lower()

            if name == "subject":
                subject = header["value"]

            elif name == "from":
                sender = header["value"]

        body = extract_body(data["payload"])

        emails.append({
            "id": message["id"],
            "sender": sender,
            "subject": subject,
            "body": body
        })

    return emails