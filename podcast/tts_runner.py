import os
import subprocess
import shutil
from mutagen.mp3 import MP3

def run_tts(text, voice="alloy", tts_dir="tts", dry_run=False):
    # Create a temporary text file for input
    temp_text_file = "tmp_input.txt"
    with open(temp_text_file, "w") as f:
        f.write(text)
    
    # Run the tts module
    # Command: python -m tts.tts [-d] -v <voice> -o output.mp3 <temp_text_file>
    # Note: TTS tool modifies output filename to output_{voice}.mp3
    output_base = "output.mp3"
    output_file = output_base.replace(".mp3", f"_{voice}.mp3")
    cmd = ["python3", "-m", "tts.tts"]
    
    if dry_run:
        cmd.append("-d")
    
    cmd.extend(["-v", voice, "-o", output_base, temp_text_file])
    
    # We need to make sure we are running from the root where tts/ is a package
    # or add tts_dir to PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(tts_dir) + os.pathsep + env.get("PYTHONPATH", "")
    
    subprocess.run(cmd, check=True, env=env)
    
    if os.path.exists(temp_text_file):
        os.remove(temp_text_file)
    
    # In dry_run mode, no output file is produced
    if dry_run:
        return None
        
    if not os.path.exists(output_file):
        raise FileNotFoundError(f"TTS tool did not produce {output_file}")
        
    return output_file

def move_audio_to_docs(src_path, dest_filename, docs_audio_dir):
    if not os.path.exists(docs_audio_dir):
        os.makedirs(docs_audio_dir)
    
    dest_path = os.path.join(docs_audio_dir, dest_filename)
    shutil.move(src_path, dest_path)
    return dest_path

def get_audio_duration(file_path):
    audio = MP3(file_path)
    return int(audio.info.length)

def get_audio_filesize(file_path):
    return os.path.getsize(file_path)
