from groq import Groq
import subprocess


class Groqy:
    def __init__(self, api_key, speaker):
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)
        self.speaker = speaker

    def answer(self, prompt):
        chat_completion = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a real-time AI assistant running on a Raspberry Pi.\n"
                        "Keep answers short and clear for spoken output.\n"
                        "Always sound friendly and helpful, like a personal voice assistant.\n"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        return chat_completion.choices[0].message.content

    def speak(self, prompt):
        self.speaker.speak(prompt)
