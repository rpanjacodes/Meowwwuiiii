import os
import subprocess
import time
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Paths
MUSIC_FOLDER = "music"
GIF_PATH = "assets/bg.gif"
WATERMARK_PATH = "assets/wc.png"
PLAYLIST_FILE = "playlist.txt"
YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2/03td-yxqh-3433-ds6g-fda0"  # Replace with your stream key

# Function to create a shuffled playlist
def update_playlist():
    files = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
    if not files:
        print("No MP3 files found! Add songs to the 'music' folder.")
        return False

    random.shuffle(files)  # Shuffle songs
    with open(PLAYLIST_FILE, "w") as f:
        for file in files:
            f.write(f"file '{file}'\n")

    return True

# Function to start FFmpeg stream
def start_stream():
    update_playlist()  # Create initial playlist

    command = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1",
        "-i", GIF_PATH,
        "-f", "concat", "-safe", "0", "-stream_loop", "-1", "-i", PLAYLIST_FILE,
        "-i", WATERMARK_PATH,
        "-filter_complex",
        "[0:v]scale=1280:720[v0];"
        "[2:v]scale=100:100[wm];"
        "[v0][wm]overlay=W-w-10:H-h-10[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "animation",
        "-b:v", "3000k", "-c:a", "aac", "-b:a", "128k",
        "-f", "flv", YOUTUBE_URL
    ]

    return subprocess.Popen(command)

# Watchdog for monitoring music folder
class MusicWatcher(FileSystemEventHandler):
    def __init__(self, process):
        self.process = process

    def on_created(self, event):
        if event.src_path.endswith(".mp3"):
            print("New MP3 detected! Updating playlist...")
            update_playlist()  # Update playlist without stopping FFmpeg

# Start the livestream
process = start_stream()
observer = Observer()
event_handler = MusicWatcher(process)
observer.schedule(event_handler, path=MUSIC_FOLDER, recursive=False)

try:
    observer.start()
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
    observer.join()
    process.terminate()
