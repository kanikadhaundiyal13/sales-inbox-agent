import re


FORBIDDEN_PATTERNS = [
    r"\$\s?\d+",
    r"\d+%\s*(discount|off)",
    r"\bguaranteed\b",
    r"\bwe guarantee\b",
    r"\bdefinitely deliver\b",
]


def validate_draft(draft):
    """
    Check an AI-generated reply for unsupported claims.
    """

    problems = []

    text = draft.lower()

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text):
            problems.append(
                f"Potential unsupported claim: {pattern}"
            )

    # Detect invented meeting availability
    availability_patterns = [
        r"\bavailable on\b",
        r"\bavailable at\b",
        r"\bmy availability\b",
    ]

    for pattern in availability_patterns:
        if re.search(pattern, text):
            problems.append(
                "Draft may contain invented meeting availability."
            )

    # Detect placeholder information
    if "[your name]" in text:
        problems.append(
            "Draft contains placeholder: [Your Name]"
        )

    if "[company]" in text:
        problems.append(
            "Draft contains placeholder: [Company]"
        )

    return problems