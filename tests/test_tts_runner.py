import os
import subprocess
import sys
import pytest
from podcast.tts_runner import run_tts, move_audio_to_docs, get_audio_duration, get_audio_filesize


def test_run_tts_success(mocker):
    """Should call tts module and return output path"""
    # Mock subprocess.run
    mock_run = mocker.patch("subprocess.run")
    # Mock os.path.exists to return True for the expected output file
    mocker.patch("os.path.exists", return_value=True)
    
    output_path = run_tts("Hello", voice="alloy", tts_dir="tts")
    
    # TTS tool modifies output filename to include voice name
    assert output_path == "output_alloy.mp3"
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert any("python" in arg for arg in args)
    assert "-m" in args
    assert "tts.tts" in args
    assert "alloy" in args


def test_run_tts_passes_output_flag(mocker):
    """run_tts should pass -o flag and expect output_{voice}.mp3.
    
    Bug: TTS tool modifies output filename to include voice name,
    e.g. output.mp3 becomes output_onyx.mp3. run_tts must account for this.
    """
    mock_run = mocker.patch("subprocess.run")
    mocker.patch("os.path.exists", return_value=True)
    
    result = run_tts("Hello", voice="onyx", tts_dir="tts")
    
    args = mock_run.call_args[0][0]
    # Check that -o flag is passed
    assert "-o" in args, "run_tts must pass -o flag to specify output file"
    # The actual output file will be output_{voice}.mp3
    assert result == "output_onyx.mp3", "Output file should include voice name"


def test_run_tts_dry_run_mode(mocker):
    """run_tts should support dry_run mode that doesn't call OpenAI API.
    
    This passes -d flag to TTS tool which prints chunks without API calls.
    """
    mock_run = mocker.patch("subprocess.run")
    mocker.patch("os.path.exists", return_value=True)
    
    run_tts("Hello", voice="onyx", tts_dir="tts", dry_run=True)
    
    args = mock_run.call_args[0][0]
    assert "-d" in args, "run_tts must pass -d flag for dry run mode"
    
    # Verify -d doesn't break other flags - voice should still be correct
    v_index = args.index("-v")
    assert args[v_index + 1] == "onyx", "-v flag must be followed by voice value, not -d"

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


def test_run_tts_creates_chunks_directory(mocker, tmp_path, monkeypatch):
    """run_tts must ensure tmp/chunks exists (the tts CLI writes chunks there)."""
    monkeypatch.chdir(tmp_path)
    mocker.patch("subprocess.run")
    (tmp_path / "output_alloy.mp3").write_bytes(b"x")

    run_tts("Hello", voice="alloy", tts_dir="tts")

    assert (tmp_path / "tmp" / "chunks").is_dir()


def test_run_tts_passes_openrouter_model_and_voice(mocker, tmp_path, monkeypatch):
    """run_tts should use OpenRouter with the selected model and voice."""
    monkeypatch.chdir(tmp_path)
    mock_run = mocker.patch("subprocess.run")
    (tmp_path / "output_Kore.mp3").write_bytes(b"x")

    run_tts("Hello", voice="Kore", tts_dir="tts", model="gemini-flash")

    args = mock_run.call_args[0][0]
    assert "-or" in args
    assert args[args.index("--model") + 1] == "gemini-flash"
    assert args[args.index("-v") + 1] == "Kore"
