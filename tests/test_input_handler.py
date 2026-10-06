import sys
import pytest
from unittest.mock import Mock
from podcast.input_handler import get_input_text, is_url, fetch_article

def test_read_from_file(tmp_path):
    """Should read text content from a file path"""
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("Hello World")
    
    assert get_input_text(str(p)) == "Hello World"

def test_read_from_file_not_found():
    """Should raise error if file doesn't exist"""
    with pytest.raises(FileNotFoundError):
        get_input_text("non_existent.txt")

def test_read_from_stdin(monkeypatch):
    """Should read from stdin when no file provided and stdin has data"""
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: False)
    monkeypatch.setattr(sys.stdin, 'read', lambda: "Stdin Content")
    
    assert get_input_text(None) == "Stdin Content"

def test_error_when_no_input(monkeypatch):
    """Should raise error when no file and stdin is a tty"""
    monkeypatch.setattr(sys.stdin, 'isatty', lambda: True)
    
    with pytest.raises(ValueError, match="No input provided"):
        get_input_text(None)


def test_is_url():
    """Should detect http(s) URLs"""
    assert is_url("https://example.com/post") is True
    assert is_url("http://example.com/post") is True
    assert is_url("post.txt") is False
    assert is_url(None) is False


def test_fetch_article_returns_text_and_metadata(mocker):
    """Should fetch a URL and return article text plus page metadata"""
    mocker.patch("trafilatura.fetch_url", return_value="<html>...</html>")
    mocker.patch("trafilatura.extract", return_value="Article body text")
    mocker.patch("trafilatura.extract_metadata",
                 return_value=Mock(title="Page Title", description="Page description"))

    text, metadata = fetch_article("https://example.com/post")

    assert text == "Article body text"
    assert metadata == {"title": "Page Title", "description": "Page description"}


def test_fetch_article_download_failure(mocker):
    """Should raise RuntimeError when the page cannot be downloaded"""
    mocker.patch("trafilatura.fetch_url", return_value=None)

    with pytest.raises(RuntimeError, match="download"):
        fetch_article("https://example.com/post")


def test_fetch_article_extraction_failure(mocker):
    """Should raise ValueError when no article text can be extracted"""
    mocker.patch("trafilatura.fetch_url", return_value="<html></html>")
    mocker.patch("trafilatura.extract", return_value=None)

    with pytest.raises(ValueError, match="extract"):
        fetch_article("https://example.com/post")


def test_fetch_article_without_metadata(mocker):
    """Should return empty title/description when page has no metadata"""
    mocker.patch("trafilatura.fetch_url", return_value="<html></html>")
    mocker.patch("trafilatura.extract", return_value="Body")
    mocker.patch("trafilatura.extract_metadata", return_value=None)

    text, metadata = fetch_article("https://example.com/post")

    assert text == "Body"
    assert metadata == {"title": "", "description": ""}
