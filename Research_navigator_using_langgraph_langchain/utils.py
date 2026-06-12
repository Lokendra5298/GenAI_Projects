# utils.py
# Placeholder for any utilities
def truncate_text(text: str, max_length: int = 1000) -> str:
    return text[:max_length] + "..." if len(text) > max_length else text