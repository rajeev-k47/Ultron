import subprocess
import signal
import os

from matrix.write import Matrix


class StreamPlayer:
    def __init__(self, matrix):
        self.proc = None
        self.matrix = matrix

    def play(self, query):
        self.stop()

        prev = self.matrix.get_mode()
        self.matrix.write(101)

        ytdlp = os.path.join(os.getcwd(), "dep", "yt-dlp")
        cmd = f'{ytdlp} -f bestaudio ytsearch:"{query}" -o - 2>/dev/null | ffplay -nodisp -autoexit -i - &>/dev/null'
        self.proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
        self.matrix.write(prev)

    def stop(self):
        if self.proc:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            self.proc = None
