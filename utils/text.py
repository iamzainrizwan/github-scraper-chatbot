def strip_md(text: str) -> str:
    return text.replace("**", "").replace("###", "").replace("##", "")
