import os
import subprocess
import pytest
from podcast.tts_runner import run_tts, move_audio_to_docs, get_audio_duration, get_audio_filesize

def test_run_tts_success(mocker):
    """Should call tts module and return output path"""
    # Mock subprocess.run
    mock_run = mocker.patch("subprocess.run")
    # Mock os.path.exists to return True for the expected output file
    mocker.patch("os.path.exists", return_value=True)
    
    output_path = run_tts("Hello", voice="alloy", tts_dir="tts")
    
    assert output_path == "output.mp3"
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert any("python" in arg for arg in args)
    assert "-m" in args
    assert "tts.tts" in args
    assert "alloy" in args

def test_move_audio_to_docs(tmp_path):
    """Should move mp3 file to docs/audio/ with new name"""
    audio_file = tmp_path / "output.mp3"
    audio_file.write_text("audio content")
    
    docs_audio_dir = tmp_path / "docs" / "audio"
    docs_audio_dir.mkdir(parents=True)
    
    new_path = move_audio_to_docs(str(audio_file), "new_name.mp3", str(docs_audio_dir))
    
    assert os.path.exists(new_path)
    assert os.path.basename(new_path) == "new_name.mp3"
    assert not os.path.exists(str(audio_file))

def test_get_audio_duration(mocker, tmp_path):
    """Should return duration in seconds from mp3 file"""
    # Create a dummy file so mutagen doesn't complain about file not found
    f = tmp_path / "dummy.mp3"
    f.write_text("dummy content")
    
    # Mock MP3 class to avoid actual file parsing
    mock_mp3_class = mocker.patch("podcast.tts_runner.MP3")
    mock_mp3_instance = mock_mp3_class.return_value
    mock_mp3_instance.info.length = 123.45
    
    duration = get_audio_duration(str(f))
    assert duration == 123

def test_get_audio_filesize(tmp_path):
    """Should return file size in bytes"""
    f = tmp_path / "test.mp3"
    content = "some audio data"
    f.write_text(content)
    
    assert get_audio_filesize(str(f)) == len(content)
