import sys
import pytest
from publish import main

def test_main_stdin_pipe_interactive_fixed(mocker, tmp_path):
    """Should not raise EOFError when stdin is piped but interactive input is needed"""
    # Mock input text from stdin pipe
    mocker.patch("publish.get_input_text", return_value="Some piped text")
    mocker.patch("publish.load_podcast_config", return_value={})
    mocker.patch("publish.load_episodes", return_value=[])
    mocker.patch("publish.run_tts", return_value="output.mp3")
    mocker.patch("publish.get_audio_duration", return_value=100)
    mocker.patch("publish.get_audio_filesize", return_value=1024)
    mocker.patch("publish.move_audio_to_docs")
    mocker.patch("publish.generate_filename")
    mocker.patch("publish.create_episode")
    mocker.patch("publish.save_episodes")
    mocker.patch("publish.generate_site")
    mocker.patch("publish.commit_episode")

    # Mock stdin.isatty to False (simulating a pipe)
    mocker.patch("sys.stdin.isatty", return_value=False)
    
    # Mock open('/dev/tty')
    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    
    # Mock input() to return values
    m_input = mocker.patch("builtins.input", side_effect=["Title", "Desc", "alloy"])
    
    # This should now pass without EOFError
    main(["--no-commit"])
    
    assert m_input.call_count == 3
