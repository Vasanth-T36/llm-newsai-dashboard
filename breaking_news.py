def detect_breaking(title):

    keywords = [
    "breaking",
    "urgent",
    "alert",
    "just in",
    "live"
    ]

    title_lower = title.lower()

    for k in keywords:
        if k in title_lower:
            return True

    return False