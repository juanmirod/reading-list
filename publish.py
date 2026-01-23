import argparse
import sys
import os
import json
from podcast.input_handler import get_input_text
from podcast.episodes import load_episodes, save_episodes, create_episode, generate_filename
from podcast.tts_runner import run_tts, move_audio_to_docs, get_audio_duration, get_audio_filesize
from podcast.site_generator import generate_site
from podcast.git_ops import commit_episode

def load_podcast_config(file_path="podcast.json"):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_args(args):
    parser = argparse.ArgumentParser(description="Podcast CLI Uploader")
    parser.add_argument("file", nargs="?", help="Input text file (optional if using stdin)")
    parser.add_argument("-t", "--title", help="Episode title")
    parser.add_argument("-d", "--description", help="Episode description")
    parser.add_argument("-v", "--voice", help="Voice selection")
    parser.add_argument("--no-push", dest="push", action="store_false", help="Skip git push")
    parser.add_argument("--no-commit", dest="commit", action="store_false", help="Skip git commit")
    parser.set_defaults(push=True, commit=True)
    return parser.parse_args(args)

def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])
    
    # 1. Get input text
    text = get_input_text(args.file)
    
    # Re-open /dev/tty for interactive input if stdin was a pipe
    if not sys.stdin.isatty():
        try:
            sys.stdin = open('/dev/tty')
        except (OSError, IOError):
            # Fallback if /dev/tty is not available (e.g. in some CI environments)
            pass

    # 2. Get metadata (interactive if not provided)
    title = args.title
    if not title:
        title = input("Episode Title: ")
        
    description = args.description
    if not description:
        description = input("Episode Description: ")
        
    voice = args.voice
    if not voice:
        voice = input("Voice (alloy, ash, coral, echo, fable, onyx, nova, sage, shimmer) [alloy]: ") or "alloy"
        
    # 3. Load configs
    podcast_config = load_podcast_config()
    episodes = load_episodes("episodes.json")
    
    # 4. Run TTS
    print(f"Converting text to speech with voice '{voice}'...")
    output_mp3 = run_tts(text, voice=voice)
    
    # 5. Process audio
    duration = get_audio_duration(output_mp3)
    filesize = get_audio_filesize(output_mp3)
    filename = generate_filename(title)
    
    print(f"Moving audio to docs/audio/{filename}...")
    dest_path = move_audio_to_docs(output_mp3, filename, "docs/audio")
    
    # 6. Update metadata
    new_episode = create_episode(title, description, filename, duration, filesize)
    episodes.insert(0, new_episode)
    save_episodes("episodes.json", episodes)
    
    # 7. Regenerate site
    print("Regenerating site...")
    generate_site("templates", podcast_config, episodes, "docs")
    
    # 8. Git operations
    if args.commit:
        print("Committing changes...")
        files_to_add = ["episodes.json", dest_path, "docs/feed.xml", "docs/index.html"]
        commit_episode(title, files_to_add, push=args.push)
        
    print("Done!")

if __name__ == "__main__":
    main()
