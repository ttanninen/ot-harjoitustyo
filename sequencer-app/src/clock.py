### AI generated code begins ###

import time
import threading
import sys

# How long before the deadline we stop sleeping and start busy-waiting.
# 2 ms gives comfortable margin for Windows (~15 ms sleep granularity).
_SPINWAIT_THRESHOLD = 0.002


class MasterClock:
    """
    High-precision master clock that runs in its own dedicated thread.

    The thread keeps the OS scheduler aware that something time-sensitive is
    running, which reduces wake-up latency for the sequencer thread on all
    platforms. On Windows it also activates high-resolution timer mode.

    Usage:
        clock = MasterClock()
        clock.start()
        t = clock.get_ticks()  # milliseconds since start
        clock.stop()
    """

    def __init__(self):
        self._start: float | None = None
        self._running = False
        self._thread: threading.Thread | None = None

    def start(self):
        if self._running:
            return

        # On Windows, reduce the system timer resolution from ~15 ms to ~1 ms
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.winmm.timeBeginPeriod(1)

        self._start = time.perf_counter()
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True, name="MasterClock")
        self._thread.start()

    def stop(self):
        self._running = False

        if sys.platform == "win32":
            import ctypes
            ctypes.windll.winmm.timeEndPeriod(1)

    def get_ticks(self) -> float:
        """Elapsed milliseconds since start(). Thread-safe."""
        if self._start is None:
            return 0.0
        return (time.perf_counter() - self._start) * 1000.0

    def _run(self):
        # Keeps the thread alive with minimal CPU use. The short sleep lets
        # the OS know this thread cares about timer precision without burning
        # a core.
        while self._running:
            time.sleep(0.0001)  # yield for ~100 µs


def _precise_sleep(seconds: float):
    """
    Sleep with high precision across platforms.

    Sleeps via the OS for the bulk of the wait, then busy-waits the final
    _SPINWAIT_THRESHOLD seconds. Accurate to ~50-100 µs on Windows and
    ~10 µs on Linux/macOS.
    """
    if seconds <= 0:
        return

    deadline = time.perf_counter() + seconds

    sleep_duration = seconds - _SPINWAIT_THRESHOLD
    if sleep_duration > 0:
        time.sleep(sleep_duration)

    # Busy-wait the final 2 ms
    while time.perf_counter() < deadline:
        pass


# ---------------------------------------------------------------------------
# Module-level interface
# ---------------------------------------------------------------------------

_master = MasterClock()


def start():
    """Start the master clock thread. Call once at application startup."""
    _master.start()


def stop():
    """Stop the master clock thread. Call once at application shutdown."""
    _master.stop()


def get_ticks() -> float:
    """Elapsed milliseconds since start()."""
    return _master.get_ticks()


def tick(target_ms: float = 0.0):
    """Sleep precisely for target_ms milliseconds."""
    if target_ms > 0:
        _precise_sleep(target_ms / 1000.0)

### AI-Generated code ends