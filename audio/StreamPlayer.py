import subprocess
import signal
import os


class StreamPlayer:
    def __init__(self):
        self.proc = None

    def play(self, query):
        self.stop()
        cmd = f'./dep/yt-dlp -f bestaudio ytsearch:"{query}" -o - 2>/dev/null | ffplay -nodisp -autoexit -i - &>/dev/null'
        self.proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

    def stop(self):
        if self.proc:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            self.proc = None
