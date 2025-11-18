
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

---
# November 18 2025

## 1. Summary of Activities

Today’s session focused on improving the overall structure, flexibility, and performance of the template‑matching workflow. The work included refactoring utility scripts, enhancing the rotated‑template generator, adding video support to notebooks, and experimenting with reduced template sets for faster processing.

## 2. Key Technical Work Completed

### 2.1 Refactored File Dialog Utilities

- Improved the design of `file_dialog_utils` to make it more modular.
- Added support for:
    - Selecting **multiple images**
    - Selecting **videos**
    - Returning cleaner, more consistent data structures
    
- These improvements prepare the system for calibration workflows that use multiple frames or mixed media.

### 2.2 Updated Rotated Template Generator

- Added support for **non‑integer angle intervals** (e.g., 0.5°, 0.25°, 1.0°, 1.25°).
- Updated rotation range to **−181.0° → +181.0° with 0.1° increments**, preserving full angular coverage while cutting template count nearly in half.
- Identified a high‑quality rotation configuration:
    - `crop_factor = 0.65`
    - `keep_size = False`
    
- This reliably removes black corners after rotation, though shrinking templates introduces **scale mismatch** that affects matching behaviour.

### 2.3 Major Updates to Multiple Template Matching Notebook

- Removed leftover code from the original simple template‑matching notebook.
- Implemented a unified pipeline working with **both images and videos**.
- Added reusable helper function:
    - `match_best_template_on_frame(frame_bgr, ...)`
- Added:
    - Live frame‑by‑frame rendering in Jupyter
    - Optional annotated video writer
    - Resolution fallback extraction
    - FPS‑aware configuration

### 2.4 Video Support Added

- The system can now accept **video as the target source**.
- Each frame is processed for best pocket match.
- Bounding boxes are rendered live.
- Annotated output videos can be saved for analysis.

### 2.5 Reduced Template Set for Video Efficiency

- Full set of ~28,804 rotated templates is computationally impossible for per‑frame video detection.
- Reduced the working set to **11 templates** for feasibility testing.
- Performance: 333 frames × 11 templates = 3,663 comparisons → realistic runtime.
- Generated a complete annotated video output.
- Key insight: **template matching is too expensive to perform at scale; heavy work must be moved to calibration only.**

### 2.6 Pipeline Strategy Clarified

- **Calibration (once per wheel):**
    - Use large template sets and heavy matching.
    - Identify 3–6 reliable pockets.
    - Fit a circle/ellipse to derive the wheel’s geometry.
    - Compute all pocket coordinates mathematically.

- **Runtime (per spin):**
    - Use 1–2 strong templates to track wheel rotation.
    - Use YOLO later for ball detection.
    - Determine the landed pocket from angle matching.

## 3. Discoveries & Insights

### High Score ≠ Correct Match (Important Finding)

- Using rotation‑generated templates (−181° → +181°) produced **very high scores (~0.925)** yet often matched **the wrong pocket**.
- A manually chosen template, despite producing a **lower score (~0.571)**, identified the **correct pocket**.

This shows that:

- Roulette wheel pockets contain **repetitive patterns**.
- Auto‑rotated templates (especially when cropped to 65%) are too **generic**, capturing only local features.
- Manually selected templates contain **implicit context** (neighbor pockets + separators).
- Therefore, **high correlation does not guarantee correctness**.

### Updated Implications

- Rotated template batches are best used for **coarse search**, not final decisions.
- Larger, contextual templates remain **more discriminative**.
- Template matching belongs in the **calibration stage**, not constant per‑frame detection.

## 4. Where We Are → Where We Left Off

### Achieved Today

- Fully functional pipeline for image and video matching.
- Modular utilities and template loading.
- Annotated video generation.
- Validation that template matching must be limited to calibration.
- A clear, mathematically grounded pipeline direction.

### Next Steps

- Create a **calibration notebook** to detect 3–6 pockets on a high‑quality frame.
- Fit an ellipse and generate all 37 pocket coordinates.
- Implement wheel‑rotation tracking using minimal templates.
- Begin early YOLO ball‑tracking integration.

## 5. Reflection

Today transformed the project from experimental exploration into a defined, scalable pipeline. The major conceptual leap was recognising that template matching is useful **only for calibration**, while rotation tracking and ball detection form the runtime backbone. The discovery that high correlation does not imply correctness further refines the methodological approach.

This steady refinement is building a strong foundation for the dissertation's methodology.