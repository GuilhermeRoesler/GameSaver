"""Window / taskbar icon helpers (especially Windows native HICON)."""

from __future__ import annotations

import os
import sys

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QWidget

from ..constants import ICON_ICO_PATH, ICON_PNG_PATH


def resolve_icon_path() -> str | None:
    """Prefer .ico on Windows (native taskbar); fall back to PNG."""
    candidates: list[str] = []
    if sys.platform == 'win32':
        candidates.append(ICON_ICO_PATH)
    candidates.extend([ICON_PNG_PATH, ICON_ICO_PATH])
    for path in candidates:
        if path and os.path.exists(path):
            return path
    return None


def load_app_icon() -> QIcon:
    path = resolve_icon_path()
    if path is None:
        return QIcon()

    icon = QIcon(path)
    # Ensure common taskbar/title-bar sizes are present even when source is a single PNG.
    if path.lower().endswith('.png'):
        pixmap = QPixmap(path)
        for size in (16, 24, 32, 48, 64, 128, 256):
            icon.addPixmap(pixmap.scaled(size, size))
    return icon


def apply_native_window_icon(window: QWidget, icon_path: str | None = None) -> None:
    """Force WM_SETICON so the Windows taskbar uses our .ico, not a blank/python icon."""
    if sys.platform != 'win32':
        return

    path = icon_path or resolve_icon_path()
    if not path or not path.lower().endswith('.ico') or not os.path.exists(path):
        return

    try:
        import ctypes
    except ImportError:
        return

    user32 = ctypes.windll.user32
    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x0010
    WM_SETICON = 0x0080
    ICON_SMALL = 0
    ICON_BIG = 1

    abs_path = os.path.abspath(path)
    hwnd = int(window.winId())

    # Keep signatures loose — incorrect argtypes here can crash the process on Windows.
    hicon_small = user32.LoadImageW(0, abs_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)
    hicon_big = user32.LoadImageW(0, abs_path, IMAGE_ICON, 32, 32, LR_LOADFROMFILE)
    if hicon_small:
        user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon_small)
    if hicon_big:
        user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon_big)
