import sys
import os
import trafilatura


def is_url(source):
    return bool(source) and source.startswith(("http://", "https://"))


def _clean(value):
    """Collapse whitespace/newlines from metadata values."""
    return " ".join((value or "").split())


def fetch_article(url):
    """Download `url` and return (article_text, metadata).

    The text contains the main article content only (like Firefox reader
    mode). metadata is a dict with 'title' and 'description' ('' when the
    page does not provide them).
    """
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise RuntimeError(f"Could not download {url}")

    text = trafilatura.extract(downloaded, output_format="txt",
                               include_comments=False, include_tables=False)
    if not text:
        raise ValueError(
            f"Could not extract article text from {url} (is it JS-rendered "
            "or paywalled?). Fetch the text manually and pipe it instead.")

    meta = trafilatura.extract_metadata(downloaded)
    metadata = {
        "title": _clean(getattr(meta, "title", "")) if meta else "",
        "description": _clean(getattr(meta, "description", "")) if meta else "",
    }
    return text, metadata


def get_input_text(file_path=None):
    if file_path:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, 'r') as f:
            return f.read()

    if not sys.stdin.isatty():
        return sys.stdin.read()

    raise ValueError("No input provided. Provide a file path or pipe text via stdin.")
