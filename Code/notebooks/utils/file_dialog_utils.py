import tkinter as tk
from tkinter import filedialog
import cv2

def pick_file(
    title="Select a file",
    filetypes=(("All files", "*.*"),),
):
    """Open a blocking file picker dialog and return the selected path or ''."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    path = filedialog.askopenfilename(title=title, filetypes=filetypes)

    root.destroy()
    return path


def pick_image_cv2(
    title="Select an image",
    filetypes=(
        ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"),
        ("All files", "*.*"),
    ),
):
    """Open a file dialog, load the image with cv2, and return (image, path)."""
    path = pick_file(title=title, filetypes=filetypes)
    if not path:
        raise ValueError("No file selected.")

    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Failed to load image from: {path}")

    return img, path


def pick_folder(title="Select a folder"):
    """Open a folder picker dialog and return the selected folder path or ''. """
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    path = filedialog.askdirectory(title=title)

    root.destroy()
    return path


def pick_folder_strict(title="Select a folder"):
    """Open a folder picker and raise ValueError if nothing selected."""
    path = pick_folder(title)
    if not path:
        raise ValueError("No folder selected.")
    return path