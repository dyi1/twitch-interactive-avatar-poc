import os
import subprocess

class TwitchClient:
    def __init__(self): 
        self.twitch_stream_key = os.getenv("TWITCH_STREAM_KEY")

    def _get_stream_url(self):
        stream_url = f"rtmp://sjc06.contribute.live-video.net/app/{self.twitch_stream_key}"
        return stream_url

    def stream_to_twitch(self, input_file="test_data/video2.mov"):
        rtmp_url = self._get_stream_url()
        ffmpeg_command = [
            "ffmpeg",
            "-re",
            "-i", input_file,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-maxrate", "3000k",
            "-bufsize", "6000k",
            "-c:a", "aac",
            "-b:a", "160k",
            "-ar", "44100",
            "-f", "flv",
            rtmp_url
        ]
        # Run ffmpeg as a process
        os.execvp("ffmpeg", ffmpeg_command)

        