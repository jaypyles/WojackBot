# LOCAL
from WojackBot.utils.constants import ERROR_MESSAGE


def validate_caption(caption_strip: str) -> bool:
    """Validates if the caption is five words and not an error message."""
    if caption_strip == ERROR_MESSAGE:
        return False

    return len(caption_strip.split()) == 5
