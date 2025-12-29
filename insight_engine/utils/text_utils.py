"""Utility functions."""

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def extract_article_sections(article_text: str) -> dict:
    """
    Extract different sections from an article.
    
    Args:
        article_text: The full article text
        
    Returns:
        Dictionary with sections (title, introduction, body, conclusion)
    """
    lines = article_text.split("\n")
    sections = {
        "title": "",
        "introduction": "",
        "body": "",
        "conclusion": "",
    }
    
    # Simple heuristic: first line is title, first paragraph is intro
    if lines:
        sections["title"] = lines[0].strip()
        
    # Rest is body (simplified)
    sections["body"] = article_text
    
    return sections
