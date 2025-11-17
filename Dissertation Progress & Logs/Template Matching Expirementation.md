
# November 16-17 2025

## 1. **Summary of Activities**

Today’s work focused on exploring **template matching** as the first experimental approach for detecting roulette pockets. Activities included:

- Extracting a cropped “3” pocket from a wheel image.
- Upscaling the tiny template using OpenCV super-resolution.
- Sharpening and cleaning the template.
- Running classical `cv2.matchTemplate`.
- Generating **rotated variants** of the template.
- Testing multi-angle and multi-scale matching.
- Capturing **four wheel scenarios** where the “3” pocket appears at:
    - **12 o’clock**
    - **3 o’clock**
    - **6 o’clock**
    - **9 o’clock**
- Capturing **four larger templates** of the “3” pocket (including ~70% of neighbouring pockets).
- Testing each template against each wheel scenario.

---
## 2. **What Approaches Were Tried**

### **2.1 Simple template matching (raw template)**

- Used the very small cropped “3”.
- Direct matching worked partially (scores ~0.98 when scale was identical).
- Confirmed template matching requires near-identical scale.

---
### **2.2 Upscaled template (super-resolution)**

- Used EDSR ×4 to upscale the tiny template.
- Result: **significantly worse matching**.
- Reason: scale mismatch + texture distortion.

---
### **2.3 Sharpening (Gaussian + Unsharp Mask)**

- Applied sharpening post-upscaling.
- Improved visuals but **did not improve matching**.
- Discovery: clarity < scale consistency.

---
### **2.4 Rotated templates**

- Initially created rotated templates, but black corner regions interfered.
- Implemented padded-rotation + crop pipeline.
- Improved visually, but matching still weak due to template being too small.

---
### **2.5 Multi-template sweep**

- Automatically tested all rotated templates.
- Code pipeline worked perfectly.
- But the small template produced inconsistent correlation.

---
### **2.6 NEW: Larger template matching (today’s progress)**

- Took **four new screenshots** of the "3" pocket, each containing:
    - The "3" pocket
    - Roughly **70% of neighbouring pockets**
- Matched each of these templates against:
    - 12 o'clock “3” scenario
    - 3 o'clock scenario
    - 6 o'clock scenario
    - 9 o'clock scenario

**Result:**

- **Significantly improved matching accuracy.**
- Templates with neighbouring context consistently produced strong detections.
- This validates the earlier hypothesis: **larger spatial context is crucial**.
---
## 3. **Key Discoveries**

### 🔍 **(1) Template scale is critical**

Template matching breaks if the scale is off even slightly.

### 🔍 **(2) The first tiny template was too small**

~20 px tall → insufficient.

### 🔍 **(3) Spatial context dramatically improves matching**

Including neighbouring pockets produced **successful recognitions today**.

### 🔍 **(4) Upscaling an already blurry template hurts performance**

Super-resolution alters texture.

### 🔍 **(5) Rotation requires clean templates with no black corners**

Padded-rotation + crop solves this, but is dependent on input quality.

### 🔍 **(6) Template matching is viable when template quality & context are good**

Today’s successful matches confirmed this.

---

## 4. **Where We Are → Where We Left Off**

### ✔ Current Status

- Template matching **failed** with tiny isolated crops.
- Template matching **succeeded** today with larger templates including neighbouring pockets.
- Rotation-matching pipeline is implemented but depends on template quality.

### ❗ Main Bottleneck

- High-quality, properly scaled templates are essential.

### ⭐ Today’s major improvement

- Using larger cropped templates resulted in **reliable matches** in all four wheel scenarios.

---
## 5. **Next Steps / Future Work**

### **Approach A — Use even larger templates**

Include:
- Neighbouring pockets
- Separator bars
- Local rim geometry

### **Approach B — Multi-pocket identification**

- Create templates for a few pockets.
- Detect their coordinates.
- Fit an **ellipse** around pocket centres.
- Infer all other pocket positions mathematically.

### **Approach C — Build a high-quality template dataset**

From:
- Higher-resolution frame(s)
- Synthetic image generation
- Stabilised screenshots

### **Approach D — Move to video processing**

Once the still-image pipeline is stable:
- Run matching per frame
- Track pocket position across time
- Start thinking about spin-angle mapping

---

## 6. **Reflection**

Today marks a **turning point** for the template matching experiment:
- Early failures were due to poor initial template quality.
- Larger templates with contextual information **work very well**.
- The experiment now has a clear path forward.

This iterative process—failing small, learning, and refining—is exactly what strengthens the dissertation’s methodology.


