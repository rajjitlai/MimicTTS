import sys
import threading
import time

SPINNER_FRAMES = ["|", "/", "-", "\\"]


class TTSProgressStreamer:
    """
    A HuggingFace-compatible streamer that displays a live spinner,
    token counter, and elapsed time during TTS generation.

    Runs a background thread that updates the terminal in-place.
    Token counts are incremented via put() as the model generates.
    """

    def __init__(self) -> None:
        self._token_count = 0
        self._start = time.time()
        self._done = False
        self._lock = threading.Lock()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        frame = 0
        while not self._done:
            elapsed = time.time() - self._start
            with self._lock:
                tokens = self._token_count
            sys.stdout.write(
                f"\r  [{SPINNER_FRAMES[frame % 4]}]"
                f"  {tokens} tokens"
                f"  |  {elapsed:.1f}s elapsed  "
            )
            sys.stdout.flush()
            frame += 1
            time.sleep(0.12)

    def put(self, value) -> None:
        """Called by HuggingFace generate() for each new batch of tokens."""
        with self._lock:
            # value shape: (batch, new_tokens) or scalar tensor
            if hasattr(value, "shape") and len(value.shape) >= 1:
                self._token_count += value.shape[-1]
            else:
                self._token_count += 1

    def end(self) -> None:
        """Called by HuggingFace generate() when generation is complete."""
        self._done = True
        self._thread.join(timeout=1.0)
        elapsed = time.time() - self._start
        with self._lock:
            tokens = self._token_count
        sys.stdout.write(
            f"\r  [+]  {tokens} tokens generated in {elapsed:.1f}s"
            f"{'  ' * 10}\n"
        )
        sys.stdout.flush()
