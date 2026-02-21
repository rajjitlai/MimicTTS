import sys
import threading
import time

SPINNER_FRAMES = ["|", "/", "-", "\\"]


class TTSProgressStreamer:
    """
    A HuggingFace-compatible streamer that displays a live spinner
    and elapsed time during TTS generation.

    Runs a background thread that updates the terminal in-place.

    """

    def __init__(self) -> None:
        self._start = time.time()
        self._done = False
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        frame = 0
        while not self._done:
            elapsed = time.time() - self._start
            sys.stdout.write(
                f"\r  [{SPINNER_FRAMES[frame % 4]}]"
                f"  Generating audio...  |  {elapsed:.1f}s elapsed  "
            )
            sys.stdout.flush()
            frame += 1
            time.sleep(0.12)

    def put(self, value) -> None:
        pass

    def end(self) -> None:
        """Called by HuggingFace generate() when generation is complete."""
        self._done = True
        self._thread.join(timeout=1.0)
        # Clear the line
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()
