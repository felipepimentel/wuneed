import os
import tempfile
from pytube import YouTube
import whisper

def download_youtube_video(url: str) -> str:
    """Download audio from a YouTube video."""
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        audio_stream.download(output_path=os.path.dirname(temp_file.name), filename=os.path.basename(temp_file.name))
        return temp_file.name

def transcribe_video(source: str) -> str:
    """Transcribe audio from a video file or URL."""
    model = whisper.load_model("base")
    
    if source.startswith("http"):
        # Assume it's a YouTube URL
        audio_file = download_youtube_video(source)
    else:
        # Assume it's a local file
        audio_file = source
    
    try:
        result = model.transcribe(audio_file)
        return result["text"]
    finally:
        if source.startswith("http"):
            os.unlink(audio_file)  # Clean up temporary file