import tkinter as tk
from tkinter import filedialog
import cv2

def pick_file(
    title="Select a file",
    filetypes=(("All files", "*.*"),),
):
    """Open a blocking file picker dialog and return the selected path or ''."""
    root = tk.Tk()
    root.withdraw()               # Hide the main window
    root.attributes("-topmost", True)  # Bring dialog to front

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
    """
    Open a file dialog, load the image with cv2, and return (image, path).
    Raises ValueError if nothing selected or image can't be loaded.
    """
    path = pick_file(title=title, filetypes=filetypes)
    if not path:
        raise ValueError("No file selected.")

    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Failed to load image from: {path}")

    return img, path
