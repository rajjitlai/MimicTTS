import sys
import threading
import time

SPINNER_FRAMES = ["|", "/", "-", "\\"]


class TTSProgressSpinner:
    """
    A live spinner and elapsed timer that runs in a background thread.
    Use as a context manager to wrap long-running operations.
    """

    def __init__(self) -> None:
        self._start = time.time()
        self._done = False
        self._thread = threading.Thread(target=self._run, daemon=True)

    def __enter__(self) -> "TTSProgressSpinner":
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._done = True
        self._thread.join()

        # Completely erase the spinner line from the terminal
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()

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
