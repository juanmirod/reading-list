import os
import subprocess
import sys
import pytest
from podcast.tts_runner import run_tts, move_audio_to_docs, get_audio_duration, get_audio_filesize


def test_tts_module_imports_without_numpy():
    """TTS module should be importable without numpy for OpenAI/Google TTS.
    
    Bug: numpy was imported at top level but only needed for local_tts().
    This caused ImportError when using OpenAI TTS without numpy installed.
    """
    # Temporarily remove numpy from sys.modules to simulate it not being installed
    numpy_modules = {k: v for k, v in sys.modules.items() if 'numpy' in k}
    for mod in numpy_modules:
        del sys.modules[mod]
    
    # Also temporarily make numpy unimportable
    import builtins
    original_import = builtins.__import__
    
    def mock_import(name, *args, **kwargs):
        if name == 'numpy' or name.startswith('numpy.'):
            raise ModuleNotFoundError(f"No module named '{name}'")
        return original_import(name, *args, **kwargs)
    
    builtins.__import__ = mock_import
    
    try:
        # Remove tts.tts from modules cache to force re-import
        tts_modules = [k for k in sys.modules.keys() if k.startswith('tts.')]
        for mod in tts_modules:
            del sys.modules[mod]
        
        # This should NOT raise ModuleNotFoundError for numpy
        # The tts module should be importable for OpenAI/Google TTS
        import tts.tts as tts_module
        
        # Verify the module loaded and has the expected functions
        assert hasattr(tts_module, 'openai_tts')
        assert hasattr(tts_module, 'google_tts')
        assert hasattr(tts_module, 'local_tts')
    finally:
        # Restore original import
        builtins.__import__ = original_import
        # Restore numpy modules
        sys.modules.update(numpy_modules)

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


def test_run_tts_passes_output_flag(mocker):
    """run_tts should pass -o output.mp3 to the TTS command.
    
    Bug: TTS tool creates tmp/tts_{timestamp}_{voice}.mp3 by default,
    but run_tts expects output.mp3. Must pass -o flag explicitly.
    """
    mock_run = mocker.patch("subprocess.run")
    mocker.patch("os.path.exists", return_value=True)
    
    run_tts("Hello", voice="onyx", tts_dir="tts")
    
    args = mock_run.call_args[0][0]
    # Check that -o and output.mp3 are in the command
    assert "-o" in args, "run_tts must pass -o flag to specify output file"
    output_index = args.index("-o")
    assert args[output_index + 1] == "output.mp3", "Output file should be output.mp3"

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
