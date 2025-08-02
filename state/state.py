import json
from pathlib import Path


class State:
    def __init__(self):
        self.file = Path("ultron_static.json")

    def save_state(self, state: dict):
        with open(self.file, "w") as f:
            json.dump(state, f)

    def load_state(self) -> dict:
        if self.file.exists():
            with open(self.file, "r") as f:
                return json.load(f)
        return {}
