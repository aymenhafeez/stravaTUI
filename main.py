#!/usr/bin/env python3

from stravatui.app import StravaTUIApp
from stravatui.terminal_background import is_dark, query_terminal_background


def pick_theme_name() -> str:
    bg = query_terminal_background(timeout=0.25)

    if bg is None:
        return "darktheme"

    return "darktheme" if is_dark(bg) else "lighttheme"


if __name__ == "__main__":
    app = StravaTUIApp(theme_name=pick_theme_name())
    app.run()
