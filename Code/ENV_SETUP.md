
# 🚀 **Environment Setup Guide (For Dissertation Project)**

This guide explains how to recreate the same development environment used for the Computer Vision dissertation project.

---

## 🔹 1. Install Python

Install **Python 3.12.x** from:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

✔ Make sure to check **“Add to PATH”** during installation.

---

## 🔹 2. Create and activate a virtual environment

Open a terminal inside the `Code/` folder and run:

### **Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### **Windows (Git Bash)**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### **Mac / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should now see:

```
(.venv) >
```

---

## 🔹 3. Upgrade pip

```bash
pip install --upgrade pip
```

---

## 🔹 4. Install all project dependencies (except PyTorch)

```bash
pip install -r requirements.txt
```

---

# 🔥 **5. Install PyTorch (Choose GPU or CPU version)**

PyTorch is NOT stored in `requirements.txt` because the correct version depends on:

* OS
* CUDA version
* GPU availability

Choose one option below.

---

## ⚡ **OPTION A — Install PyTorch with CUDA (GPU acceleration)**

### If the machine has an NVIDIA GPU

(e.g., RTX 20xx, 30xx, 40xx series)

Run:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

This installs the CUDA **12.1** build (compatible with RTX GPUs).

---

## 🧱 **OPTION B — Install CPU-only version (no GPU)**

For machines without an NVIDIA GPU:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

✔ Works everywhere
✔ Much smaller install
❌ Slower for training YOLO or diffusion models

---

# 🔹 6. Add the venv to Jupyter

(Only needed if using Jupyter notebooks)

```bash
python -m ipykernel install --user --name dissertation-venv --display-name "dissertation-venv"
```

Then open JupyterLab:

```bash
jupyter lab
```

Select the kernel:

```
dissertation-venv
```

---

# 🔍 7. Verify the installation

Run this Python snippet:

```python
import torch, cv2, numpy as np, pandas as pd

print("Torch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))

print("OpenCV:", cv2.__version__)
print("Numpy:", np.__version__)
print("Pandas:", pd.__version__)
```

You should see:

* Torch version
* CUDA available: True/False
* GPU name (if CUDA-enabled)
* All other library versions
