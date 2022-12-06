from urllib.parse import urlparse
from pathlib import Path


def url_has_valid_file_suffix(url: str) -> bool:
    """URL is a path with a file suffix."""

    url_path = Path(urlparse(url).path)
    return bool(url_path.suffix)
