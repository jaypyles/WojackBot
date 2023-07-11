# STL
import string


def caption_strip(caption: str) -> str:
    """Strips a caption of its punctuation and makes all lowercase"""
    return caption.translate(str.maketrans("", "", string.punctuation)).lower()
