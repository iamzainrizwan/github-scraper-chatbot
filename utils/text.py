def strip_md(text: str) -> str:
    """strips common markdown formatting characters from a string."""
    return (
        text.replace("**", "")
        .replace("###", "")
        .replace("##", "")
        .replace("#", "")
        .replace("*", "")
        .replace("_", "")
    )
