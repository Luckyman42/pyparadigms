from typing import Protocol

class Speakable(Protocol):
    def speak(self) -> str: ...
