import subprocess


class Strip:
    def __init__(self):
        self.proc = subprocess.Popen(
            [ "sudo" ,"python3", "extstrip.py"], stdin=subprocess.PIPE, text=True
        )

    def rpm(self, rpm):
        self.proc.stdin.write(f"{rpm}\n")
        self.proc.stdin.flush()
