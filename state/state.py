import json
from pathlib import Path


class State:
    def __init__(self):
        self.file = Path("ultron_static.json")
        self.default_state = {"headlight": 1, "tubelight": 0, "decor": 2}

    def init_file(self):
        if not self.file.exists():
            with self.file.open("w") as f:
                json.dump(self.default_state, f, indent=4)

    def load_state(self):
        self.init_file()
        with self.file.open("r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                self.save_state(self.default_state)
                return self.default_state

    def update_state(self, key: str, value):
        state = self.load_state()
        state[key] = value
        self.save_state(state)

    def save_state(self, state: dict):
        with self.file.open("w") as f:
            json.dump(state, f, indent=4)
