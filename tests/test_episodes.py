import json
import os
import pytest
from datetime import datetime
from podcast.episodes import load_episodes, save_episodes, create_episode, generate_filename

def test_load_episodes_empty(tmp_path):
    """Should return empty list from empty episodes.json"""
    f = tmp_path / "episodes.json"
    f.write_text("[]")
    assert load_episodes(str(f)) == []

def test_load_episodes_with_data(tmp_path):
    """Should return list of episodes from episodes.json"""
    f = tmp_path / "episodes.json"
    data = [{"title": "Ep 1"}]
    f.write_text(json.dumps(data))
    assert load_episodes(str(f)) == data

def test_save_episodes(tmp_path):
    """Should write episodes list to episodes.json"""
    f = tmp_path / "episodes.json"
    data = [{"title": "Ep 1"}]
    save_episodes(str(f), data)
    assert json.loads(f.read_text()) == data

def test_create_episode():
    """Should create episode dict with title, description, date, guid, filename"""
    episode = create_episode(
        title="My Episode",
        description="Description",
        filename="20240101-slug.mp3",
        duration=120,
        filesize=1024
    )
    assert episode["title"] == "My Episode"
    assert episode["description"] == "Description"
    assert episode["filename"] == "20240101-slug.mp3"
    assert "guid" in episode
    assert "pubDate" in episode
    assert episode["duration"] == 120
    assert episode["filesize"] == 1024

def test_generate_filename():
    """Should generate YYYYMMDD-HHMMSS-slug.mp3 format"""
    filename = generate_filename("My Episode Title")
    # Format: YYYYMMDD-HHMMSS-my-episode-title.mp3
    assert filename.endswith("-my-episode-title.mp3")
    assert len(filename.split("-")[0]) == 8 # YYYYMMDD
    assert len(filename.split("-")[1]) == 6 # HHMMSS
