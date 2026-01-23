import os
import pytest
from podcast.site_generator import render_feed_xml, render_index_html, generate_site, format_rfc2822, format_duration

def test_format_rfc2822():
    """Should format datetime string as RFC 2822"""
    # Our pubDate is already RFC 2822-ish, but let's ensure it works
    date_str = "Mon, 01 Jan 2024 12:00:00 +0000"
    assert format_rfc2822(date_str) == date_str

def test_format_duration():
    """Should format seconds as HH:MM:SS or MM:SS"""
    assert format_duration(65) == "01:05"
    assert format_duration(3665) == "01:01:05"

def test_render_feed_xml(tmp_path):
    """Should render valid RSS XML with episodes"""
    podcast_config = {
        "title": "My Podcast",
        "description": "Desc",
        "base_url": "https://example.com",
        "author": "Author",
        "image": "img.png",
        "language": "en-us"
    }
    episodes = [{
        "title": "Ep 1",
        "description": "Desc 1",
        "filename": "ep1.mp3",
        "guid": "guid1",
        "pubDate": "Mon, 01 Jan 2024 12:00:00 +0000",
        "duration": 60,
        "filesize": 1024
    }]
    
    # Create template dir and file
    template_dir = tmp_path / "templates"
    template_dir.mkdir()
    feed_template = template_dir / "feed.xml.j2"
    feed_template.write_text("<rss>{{ podcast.title }} {% for ep in episodes %}{{ ep.title }}{% endfor %}</rss>")
    
    xml = render_feed_xml(str(template_dir), podcast_config, episodes)
    assert "My Podcast" in xml
    assert "Ep 1" in xml

def test_render_index_html(tmp_path):
    """Should render HTML page with episode list"""
    podcast_config = {"title": "My Podcast"}
    episodes = [{"title": "Ep 1"}]
    
    template_dir = tmp_path / "templates"
    template_dir.mkdir(exist_ok=True)
    index_template = template_dir / "index.html.j2"
    index_template.write_text("<html>{{ podcast.title }} {% for ep in episodes %}{{ ep.title }}{% endfor %}</html>")
    
    html = render_index_html(str(template_dir), podcast_config, episodes)
    assert "My Podcast" in html
    assert "Ep 1" in html

def test_generate_site(tmp_path, mocker):
    """Should write feed.xml and index.html to docs/"""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    
    mocker.patch("podcast.site_generator.render_feed_xml", return_value="<xml/>")
    mocker.patch("podcast.site_generator.render_index_html", return_value="<html/>")
    
    generate_site("templates", {}, [], str(docs_dir))
    
    assert (docs_dir / "feed.xml").exists()
    assert (docs_dir / "index.html").exists()
