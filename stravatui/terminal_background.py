import os
import re
import select
import termios
import time
import tty

OSC11_QUERY = b"\x1b]11;?\x07"  # OSC 11 query, BEL-terminated
OSC11_RE = re.compile(
    r"11;rgb:([0-9a-fA-F]{2,4})/([0-9a-fA-F]{2,4})/([0-9a-fA-F]{2,4})"
)


def _hex_to_8bit(part: str) -> int:
    value = int(part, 16)
    nibbles = len(part)  # 2 -> 8-bit, 4 -> 16-bit
    max_value = (1 << (4 * nibbles)) - 1
    return (value * 255) // max_value


def _parse_osc11_rgb(response: str):
    match = OSC11_RE.search(response)
    if not match:
        return None
    r, g, b = match.groups()
    return (_hex_to_8bit(r), _hex_to_8bit(g), _hex_to_8bit(b))


def query_terminal_background(timeout: float = 0.12):
    """Return (r, g, b) or None if unavailable/unsupported"""
    try:
        fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
    except OSError:
        return None

    old_attrs = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        os.write(fd, OSC11_QUERY)

        deadline = time.monotonic() + timeout
        buf = bytearray()

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break

            ready, _, _ = select.select([fd], [], [], remaining)
            if not ready:
                break

            chunk = os.read(fd, 1024)
            if not chunk:
                break

            buf.extend(chunk)

            # OSC replies usually end in BEL or ST (ESC \)
            if b"\x07" in buf or b"\x1b\\" in buf:
                break

        return _parse_osc11_rgb(buf.decode("ascii", errors="ignore"))

    except Exception:
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_attrs)
        os.close(fd)


def is_dark(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb

    # relative luminance (kind of)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    return luminance < 128
