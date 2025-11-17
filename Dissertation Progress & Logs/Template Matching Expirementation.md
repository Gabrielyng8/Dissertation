
# November 16-17 2025
## 1. **Summary of Activities**

The focus of today’s work was exploring **template matching** as the first experimental approach for detecting roulette pockets. This involved:

- Extracting a cropped “3” pocket from a wheel image
- Upscaling it using OpenCV super-resolution
- Sharpening and cleaning the template
- Running classical `cv2.matchTemplate`
- Generating **many rotated variants** of the template
- Testing multi-angle and multi-scale matching
- Analysing why some attempts fail and what the pipeline needs next

---
## 2. **What Approaches Were Tried**

### **2.1 Simple template matching (raw template)**

- Loaded the wheel frame (target image) and a single cropped “3”.
- Performed direct `cv2.matchTemplate` with `TM_CCOEFF_NORMED`.

**Result:**

- Worked somewhat; score around ~0.98 for upright template.
- Confirmed matching requires template scale to be very close to the real size.

---
### **2.2 Upscaled template (super-resolution)**

Used OpenCV’s EDSR ×4 to upscale the small template.

**Result:**

- Contrary to expectation, upscaling made matching _worse_.
- Score dropped significantly.
- Reason: template became too large + texture changed from original.
- Key discovery: **template matching is extremely scale-sensitive**.

---
### **2.3 Sharpening (Gaussian + Unsharp Mask)**

Applied sharpening after upscaling.

**Result:**

- Improved visual clarity but did _not_ significantly improve matchTemplate performance.
- Again: scale mismatch > clarity mismatch.
---
### **2.4 Rotated templates (to match wheel rotation)**

Generated templates at angles from −20° to +20°.

**Initial attempt:**

- Rotating produced black corners → matchTemplate failed.

**Later improvement:**

- Implemented padded-rotation + crop strategy.
- Ensured no black corners.
- Still not enough to achieve stable matching due to template size being too small relative to wheel resolution.

---

### **2.5 Multi-template loop**

Created a loop to test all rotated variants and pick the best match.

**Result:**

- Pipeline works reliably as code.
- But visually still poor detection with the current template crop, meaning the _template quality_ is the bottleneck.

---

## 3. **Key Discoveries**

### 🔍 **(1) Template scale is critical**

Matching fails unless the template is nearly the exact same scale as the pocket in the wheel frame.

### 🔍 **(2) The cropped “3” template is too small**

The original crop is only ~20 pixels tall—insufficient detail for correlation.

### 🔍 **(3) Upscaling does not solve the resolution issue**

Upscaling changes the texture → match quality drops.

### 🔍 **(4) Rotation introduces edge artifacts unless padded/cropped**

Fixed via custom rotate-and-crop function, but still limited by poor input quality.

### 🔍 **(5) Template matching may work better with a larger spatial context**

Including:

- Entire pocket block
- Neighbouring pockets
- Separator lines  
    The shape of the _block_ is equally important as the digit itself.

### 🔍 **(6) Template matching might be viable only for some pockets**

For example:

- The **green 0** pocket (unique color)
- Bold digits with strong contrast

---
## 4. **Where We Are → Where We Left Off**

### **Current Status**

- The core template-matching pipeline (code) is implemented:
    - Basic match
    - Heatmap
    - Multi-template sweep
    - Rotated templates
- But good detection was **not** achieved with the current small template.

### **Main Bottleneck**

- The template is too small and lacks crisp structure.
- Need a higher-resolution frame or a more comprehensive template region.

---

## 5. **Next Steps / Future Work**

### **Approach A — Use a larger template**

- Re-crop the “3” as a **bigger block**:
    - Include neighbouring pockets left & right
    - Include top/bottom separators
- This gives matchTemplate a stronger structural pattern.

### **Approach B — Use multiple templates**

- Manually create templates for a few pockets that are:
    - clean
    - upright
    - representative
- After detecting 3–5 pockets, **fit an ellipse** to the pocket centres to reconstruct:
    - the wheel rim
    - the circular mapping  
        Then infer positions of all other pockets mathematically.

### **Approach C — Build a higher-quality template dataset**

- From:
    - a higher-resolution wheel frame
    - a different still image without motion blur
    - or synthetic image generation
- Extract upright patches and rotate stabilized regions.

### **Approach D — Move towards video**

Once matching is stable on still images:

- Feed frames from the roulette spin video
- Perform continuous matching per frame
- Track consistency over time
- Begin exploring pocket centroid tracking

---
## 6. **Reflection**

Even though matching did _not_ succeed today, it was still a productive session because:

- We discovered the limitations and failure conditions.
- We now know why it’s failing (template resolution + scale mismatch).
- We established a clear direction for iteration.
- The experimentation pipeline is now ready for improved templates.

This is exactly the type of iterative experimentation expected in the dissertation.

---
