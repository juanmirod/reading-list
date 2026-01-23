"""Tests for TTS module - directory creation bug fix."""
import os
import tempfile
import shutil
from unittest.mock import Mock, patch
import pytest


class TestOpenAITTSCreatesDirectory:
    """Test that openai_tts creates the output directory if it doesn't exist."""

    def test_openai_tts_creates_directory_when_missing(self):
        """openai_tts should create parent directories for the output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Path to a non-existent subdirectory
            output_path = os.path.join(tmpdir, "nonexistent", "subdir", "output.mp3")
            
            # Mock the OpenAI client to avoid actual API calls
            mock_response = Mock()
            mock_response.stream_to_file = Mock()
            
            mock_client = Mock()
            mock_client.audio.speech.create.return_value = mock_response
            
            with patch('tts.tts.tts.OpenAI', return_value=mock_client):
                from tts.tts.tts import openai_tts
                openai_tts(txt="Hello world", speech_file_path=output_path)
            
            # The directory should have been created
            assert os.path.exists(os.path.dirname(output_path))
            # stream_to_file should have been called with the path
            mock_response.stream_to_file.assert_called_once_with(output_path)


class TestGoogleTTSCreatesDirectory:
    """Test that google_tts creates the output directory if it doesn't exist."""

    def test_google_tts_creates_directory_when_missing(self):
        """google_tts should create tmp/chunks directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory so tmp/chunks is created there
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            
            try:
                # Ensure tmp/chunks doesn't exist
                assert not os.path.exists("tmp/chunks")
                
                mock_gtts = Mock()
                
                with patch('tts.tts.tts.gTTS', return_value=mock_gtts):
                    from tts.tts.tts import google_tts
                    google_tts(txt="Hello world")
                
                # The directory should have been created
                assert os.path.exists("tmp/chunks")
            finally:
                os.chdir(original_cwd)


class TestCombineChunksCreatesDirectory:
    """Test that combine_chunks creates the output directory if it doesn't exist."""

    def test_combine_chunks_creates_directory_when_missing(self):
        """combine_chunks should create output directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mock audio file to combine
            input_file = os.path.join(tmpdir, "input.mp3")
            output_path = os.path.join(tmpdir, "nonexistent", "output.mp3")
            
            # Create a minimal valid MP3 file for testing
            # We'll mock AudioSegment instead
            mock_audio = Mock()
            mock_combined = Mock()
            mock_combined.__iadd__ = Mock(return_value=mock_combined)
            
            with patch('tts.tts.tts.AudioSegment') as mock_audio_segment:
                mock_audio_segment.empty.return_value = mock_combined
                mock_audio_segment.from_file.return_value = mock_audio
                
                from tts.tts.tts import combine_chunks
                combine_chunks([input_file], output_path)
            
            # The directory should have been created
            assert os.path.exists(os.path.dirname(output_path))
