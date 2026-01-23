import pytest
import sys
from publish import parse_args, main

def test_parse_args_with_file():
    """Should parse file argument"""
    args = parse_args(["input.txt"])
    assert args.file == "input.txt"

def test_parse_args_with_options():
    """Should parse --title, --voice, --description"""
    args = parse_args(["--title", "My Title", "--voice", "coral", "--description", "Desc", "input.txt"])
    assert args.title == "My Title"
    assert args.voice == "coral"
    assert args.description == "Desc"

def test_parse_args_no_push():
    """Should parse --no-push flag"""
    args = parse_args(["--no-push", "input.txt"])
    assert args.push is False

def test_main_flow(mocker):
    """Should orchestrate all steps in correct order"""
    # Mock all dependencies
    m_input = mocker.patch("publish.get_input_text", return_value="Text")
    m_load_pod = mocker.patch("publish.load_podcast_config", return_value={"title": "Pod"})
    m_load_ep = mocker.patch("publish.load_episodes", return_value=[])
    m_gen_filename = mocker.patch("publish.generate_filename", return_value="2024-file.mp3")
    m_run_tts = mocker.patch("publish.run_tts", return_value="output.mp3")
    m_duration = mocker.patch("publish.get_audio_duration", return_value=100)
    m_filesize = mocker.patch("publish.get_audio_filesize", return_value=1024)
    m_move = mocker.patch("publish.move_audio_to_docs", return_value="docs/audio/2024-file.mp3")
    m_create_ep = mocker.patch("publish.create_episode", return_value={"title": "T"})
    m_save_ep = mocker.patch("publish.save_episodes")
    m_gen_site = mocker.patch("publish.generate_site")
    m_commit_ep = mocker.patch("publish.commit_episode")
    
    # Mock interactive prompts
    mocker.patch("builtins.input", side_effect=["Title", "Desc", "alloy"])
    
    # Run main with minimal args
    main(["input.txt"])
    
    m_input.assert_called_once_with("input.txt")
    m_run_tts.assert_called_once()
    m_move.assert_called_once()
    m_save_ep.assert_called_once()
    m_gen_site.assert_called_once()
    m_commit_ep.assert_called_once()

def test_interactive_prompt_title(mocker):
    """Should prompt for title if not provided"""
    mocker.patch("publish.get_input_text", return_value="Text")
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
    
    m_input = mocker.patch("builtins.input", side_effect=["Prompted Title", "Desc", "alloy"])
    
    main(["input.txt"])
    
    assert m_input.call_args_list[0][0][0] == "Episode Title: "
