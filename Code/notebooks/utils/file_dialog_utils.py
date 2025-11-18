import os
from pathlib import Path
from contextlib import contextmanager
from typing import List, Tuple, Literal, Union

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}
VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".m4v", ".webm"}

MediaKind = Literal["image", "video"]
ImageType = np.ndarray
VideoType = cv2.VideoCapture


# ---------- TK helpers ----------

@contextmanager
def _tk_root():
    """Context manager that creates a hidden, topmost Tk root and destroys it safely."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        yield root
    finally:
        root.destroy()


def _ask_open_file(title: str, filetypes) -> str:
    with _tk_root():
        return filedialog.askopenfilename(title=title, filetypes=filetypes)


def _ask_open_files(title: str, filetypes) -> Tuple[str, ...]:
    with _tk_root():
        return filedialog.askopenfilenames(title=title, filetypes=filetypes)


def _ask_directory(title: str) -> str:
    with _tk_root():
        return filedialog.askdirectory(title=title)


# ---------- CV2 helpers ----------

def _load_image(path: str) -> ImageType:
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Failed to load image from: {path}")
    return img


def _open_video(path: str) -> VideoType:
    cap = cv2.VideoCapture(path)
    if not cap or not cap.isOpened():
        raise ValueError(f"Failed to open video from: {path}")
    return cap


def _classify_by_ext(path: str) -> Literal["image", "video", "unknown"]:
    ext = Path(path).suffix.lower()
    if ext in IMAGE_EXTS:
        return "image"
    if ext in VIDEO_EXTS:
        return "video"
    return "unknown"


# ---------- Public API ----------

def pick_media_cv2(
    title: str = "Select an image or video",
    filetypes=(
        (
            "Media files",
            "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif;"
            "*.mp4;*.avi;*.mov;*.mkv;*.wmv;*.m4v;*.webm",
        ),
        ("All files", "*.*"),
    ),
) -> Tuple[Union[ImageType, VideoType], str, MediaKind]:
    """Open a file dialog for image or video.

    Returns:
        (data, path, kind)
            - If kind == 'image': data is a numpy array (BGR)
            - If kind == 'video': data is a cv2.VideoCapture

    Raises:
        ValueError if no file selected or media cannot be opened.
    """
    path = _ask_open_file(title=title, filetypes=filetypes)
    if not path:
        raise ValueError("No file selected.")

    kind = _classify_by_ext(path)

    if kind == "image":
        return _load_image(path), path, "image"

    if kind == "video":
        return _open_video(path), path, "video"

    # Fallback based on content (as in your original)
    try:
        img = _load_image(path)
        return img, path, "image"
    except ValueError:
        pass

    try:
        cap = _open_video(path)
        return cap, path, "video"
    except ValueError:
        pass

    raise ValueError(f"Unrecognized or unsupported media type for: {path}")


def pick_file(
    title: str = "Select a file",
    filetypes=(("All files", "*.*"),),
) -> str:
    """Open a blocking file picker dialog and return the selected path.

    Raises:
        ValueError if the user cancels.
    """
    path = _ask_open_file(title=title, filetypes=filetypes)
    if not path:
        raise ValueError("No file selected.")
    return path


def pick_image_cv2(
    title: str = "Select an image",
    filetypes=(
        ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif"),
        ("All files", "*.*"),
    ),
) -> Tuple[ImageType, str]:
    """Open a file dialog, load the image with cv2, and return (image, path)."""
    path = pick_file(title=title, filetypes=filetypes)
    img = _load_image(path)
    return img, path


def pick_images_cv2(
    title: str = "Select one or more images",
    filetypes=(
        ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif"),
        ("All files", "*.*"),
    ),
) -> Tuple[List[ImageType], List[str]]:
    """Open a multi-file dialog, load images with cv2, and return (images, paths).

    Returns:
        images: list[np.ndarray] each a BGR image
        paths:  list[str] absolute file paths for the selected images

    Raises:
        ValueError if no files selected or any image fails to load.
    """
    paths = _ask_open_files(title=title, filetypes=filetypes)
    if not paths:
        raise ValueError("No files selected.")

    images: List[ImageType] = []
    failed: List[str] = []

    for p in paths:
        try:
            images.append(_load_image(p))
        except ValueError:
            failed.append(p)

    if failed:
        raise ValueError(
            "Failed to load the following image(s):\n" + "\n".join(failed)
        )

    return images, list(paths)


def pick_video_cv2(
    title: str = "Select a video",
    filetypes=(
        ("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv;*.m4v;*.webm"),
        ("All files", "*.*"),
    ),
) -> Tuple[VideoType, str]:
    """Open a file dialog, open the video with cv2, and return (VideoCapture, path)."""
    path = pick_file(title=title, filetypes=filetypes)
    cap = _open_video(path)
    return cap, path


def pick_folder(title: str = "Select a folder") -> str:
    """Open a folder picker dialog and return the selected folder path.

    Raises:
        ValueError if the user cancels.
    """
    path = _ask_directory(title=title)
    if not path:
        raise ValueError("No folder selected.")
    return path
