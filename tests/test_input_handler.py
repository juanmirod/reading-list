import sys
import pytest
from podcast.input_handler import get_input_text

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
