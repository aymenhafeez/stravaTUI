import os
import re
import select
import sys
import termios
import tty

OSC = "\x1b]"
ST = "\x1b\\"
BEL = "\x07"


def query_terminal_background(timeout: float = 0.15):
    """
    Send OSC 11 query to get terminal background
    Return r,g,b in 0-255 range or None if unsupported
    """
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return None

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)

        # request terminal background colour
        sys.stdout.write(f"{OSC}11;?{BEL}")
        sys.stdout.flush()

        response = ""
        end_time = select.select

        # read a short response window
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            return None

        while True:
            ready, _, _ = select.select([sys.stdin], [], [], 0.02)
            if not ready:
                break
            chunk = os.read(fd, 1024).decode("utf-8", errors="ignore")
            response += chunk

            # common terminators
            if BEL in response or ST in response:
                break

        # ESC ] 11;rgb:1c1c/1e1e/2424 BEL
        # ESC ] 11;rgb:1111/2222/3333 ESC \
        match = re.search(
            r"11;rgb:([0-9a-fA-F]{2,4})/([0-9a-fA-F]{2,4})/([0-9a-fA-F]{2,4})", response
        )
        if not match:
            return None

        def to_8bit(part: str) -> int:
            value = int(part, 16)
            if len(part) == 2:
                return value
            if len(part) == 4:
                return value // 257  # 65535 -> 255

            return min(255, value)

        return tuple(to_8bit(part) for part in match.groups())

    except Exception:
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def is_dark(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb

    # relative luminance (kind of)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b

    return luminance < 128
