import json
import os
import uuid
from datetime import datetime
from slugify import slugify

def load_episodes(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

def save_episodes(file_path, episodes):
    with open(file_path, 'w') as f:
        json.dump(episodes, f, indent=2)

def create_episode(title, description, filename, duration, filesize):
    return {
        "title": title,
        "description": description,
        "filename": filename,
        "duration": duration,
        "filesize": filesize,
        "guid": str(uuid.uuid4()),
        "pubDate": datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    }

def generate_filename(title):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    slug = slugify(title)
    return f"{timestamp}-{slug}.mp3"
