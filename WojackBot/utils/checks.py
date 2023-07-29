# LOCAL
from WojackBot.utils.constants import ERROR_MESSAGE


def validate_caption(caption_strip: str) -> bool:
    """Validates if the caption is five words and not an error message."""
    if caption_strip == ERROR_MESSAGE:
        return False

    return 5 <= len(caption_strip.split()) < 8


def validate_gif(gif_query: str) -> bool:
    """Validates to make sure the gif is not an error message."""
    if gif_query == ERROR_MESSAGE:
        return False
    return True
