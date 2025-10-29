This page expands on the mentor discussion regarding synthetic bias injection and outlines how simulated and physical data will be balanced in the final methodology.

## 1) Using a €100 wheel — what you can/should do

### Can you record spins and induce bias? — Yes, with caveats

- A cheap wheel is **perfect** for an experimental prototype: you control the environment, camera, lighting, and you can intentionally alter mechanical conditions (tilt, weights, scuffs) to test sensitivity.
- It will **not** perfectly mimic a casino-grade wheel (different tolerances, bearings, friction). That’s fine — your aim is _proof of concept / calibration tool_, not commercial certification.

### How many spins to record?

Depends on the goal:

**A. CV validation (does the detection pipeline correctly label pockets?)**

- Aim: measure detection **accuracy** (per-frame/ per-spin).
- Practical target: **~200–500 spins** is usually enough to estimate CV accuracy to ± a few percentage points and build a confusion matrix. Use multiple camera angles if possible (or a few videos).
- You can split data: 70% train / 30% test (or use pre-trained detector then evaluate).

**B. Demonstrating sensitivity to mechanical change (calibration experiment)**

- Aim: show the system detects changes when you _change the wheel_ (tilt, weight).
- For visible/large induced biases (e.g., notable tilt), **hundreds of spins** per condition (e.g., 300–1000) will give stronger evidence. With a strong induced bias you may see detectable deviations with far fewer spins (100–300).
- Because you control the intervention, you can run repeated short experiments (e.g., 5 × 200 spins baseline, 5 × 200 spins tilted) to demonstrate consistent shifts.

**C. Statistical detection of small biases**

- If you wanted to _statistically prove_ a tiny pocket probability change (e.g., 2–3%), you would need very large N (tens/ hundreds of thousands). Don’t aim for that. Instead: focus on _detectable_ changes via controlled manipulations; show sensitivity threshold.
    

### Practical manipulations you can try (safe, reversible)

- **Small table tilt**: incremental angles (0.5°, 1°, 2°) using shims under one table foot.
- **Add tiny weights**: attach small weights under the rim (tape a coin) to bias rotation/freedom.
- **Fret/pocket scuff or mark**: introduce subtle friction differences.
- **Change ball initial conditions**: vary release point / speed to simulate real-world operator variance.  
    Record metadata for each run (angle, weight, ball type, camera settings).

### What to measure & report

- **CV metrics**: precision, recall, accuracy, confusion matrix for pocket labels.
- **Per-run stats**: counts per pocket, proportions, and 95% CIs.
- **Comparisons**: baseline vs manipulated runs — show effect sizes, p-values, and CIs.
- Recommended tests: chi-square for categorical frequencies (with caution on small N), Fisher exact for small counts, permutation tests, or a simple two-sample proportion test for a target pocket. Consider reporting **effect sizes** (not just p-values). For small-N you can use **bootstrap** to get confidence intervals.

---

## 2) How to convince the mentor _before_ buying a wheel

You don’t need to buy anything to prove your approach is valid. Present a clear plan and evidence that your CV / homography pipeline works on **existing videos** and that real experiments are feasible.

### Immediate things you can do (no cost)

1. **Run your CV/homography pipeline on public videos**
    - Use YouTube/stream recordings of roulette wheels (varied camera angles) to:
        - show ball detection works,
        - show you can calibrate a wheel via homography/green-0 detection,
        - produce a small table of CV accuracy (even on 50–200 annotated spins).
    - This demonstrates the **vision layer is implementable** and not just a theory.
    
2. **Create a staged simulation using a single video**
    - Take a single “fair” video and artificially rotate/shift the final angular mappings to simulate a biased wheel; run your statistical step to show it detects that change. This is _not_ fabricating final claims — it’s proof that your statistical detector responds correctly to known changes.
    
3. **Draft an experimental protocol**
    - Show the mentor a concrete plan for the physical experiment: number of spins, camera placement, controlled manipulations, how you’ll collect metadata, and which statistics you’ll run. Concrete numbers and repeatability win trust.
    
4. **Provide an evaluation plan**
    - Explain you will separate **CV validation** from **bias detection**:
        - Phase A: CV & homography accuracy (using public videos + annotated ground truth) — that demonstrates the ball→pocket pipeline works.
        - Phase B: Controlled physical tests (cheap wheel) to show the calibration tool detects mechanically induced changes.
        - Phase C (optional): limited analysis of “real-world” public streams for generalizability.

### Suggested message / pitch to your mentor

You can copy/paste this short message:

> Hi Darren — quick plan to validate the approach before I buy hardware:
> 
> 1. Run the homography + ball-tracking pipeline on several publicly available roulette videos and produce a small annotated evaluation (50–200 spins) to show detection/pocket-mapping works.
> 2. Simulate controlled “bias” on recorded video (apply angular offsets or resample positions) to demonstrate the statistical detection responds to known perturbations.
> 3. If steps 1–2 look good, proceed to buy a low-cost physical wheel and run controlled experiments (baseline vs tilted/weighted) to validate the calibration tool on real data.  
>     This plan separates CV verification from physical testing and preserves validity. Thoughts?

That shows methodical thinking and mitigates the need for immediate purchase.

---

## 3) On synthetic bias injection — a defensible stance

- Your mentor was right to be cautious: **fabricating data and claiming it as real** is bad.
- But **synthetic bias for validation** is acceptable _if_ it is:
    - Explicitly described as simulated in the methodology, and
    - Used only to show _sensitivity_ of the detection algorithm (not to claim real-world prevalence).
    
- Best practice: combine both approaches — simulation to quantify detection limits, and real physical manipulations to show real-world detectability.

---

## 4) Short experimental checklist (to include in your SOI/methods)

- Camera: fixed mount, documented height & focal length.
- Lighting: constant, avoid glare.
- Ball: note size/material.
- Spins per condition: aim for 200–500 (CV) and 200–1000 per manipulated condition (calibration test).
- Metadata per run: wheel ID, camera, spin number, manipulation type, exact shim height/weight.
- Evaluation metrics: CV confusion matrix; pocket frequency tables; effect sizes; bootstrap CIs; chi-square / permutation tests.

---

## 5) Quick recommended wording for your SOI (to reassure mentor)

> “Phase 1 will validate the CV and geometric calibration pipeline using publicly available roulette footage and annotated ground truth (50–200 spins). Phase 2 will perform controlled physical experiments on a consumer roulette wheel (baseline and deliberate mechanical perturbations such as tilt and localized weight) to validate the calibration tool’s sensitivity. Simulations will be used only to quantify algorithmic detection limits — all claims about real-world detection will be supported by physical experiments.”

---

### Bottom line (TL;DR)

- Buy the wheel **after** you demonstrate the CV/homography pipeline works on public videos and present a detailed experimental plan.
- For CV validation: **~200–500 spins** is a realistic start.
- For showing you can detect induced bias: run multiple controlled runs (hundreds of spins each), document manipulations, and use repeated experiments.
- Synthetic bias can be used for _algorithm validation_ but must be transparently labelled and paired with physical experiments for credibility.

---

Optional work:

- Draft the **detailed experimental protocol** (step-by-step) you can show Darren, including exact run counts and how to alter tilt/weight safely; **or**
- Generate a small **evaluation template** (CSV columns, metrics to compute, plotting checklist) you can use when you start collecting data.

---

## 🧩 TL;DR / Summary

This page expands on the mentor discussion regarding the **synthetic bias injection issue**.  
It outlines how I plan to balance **simulated** and **real physical data** within the roulette calibration system.

**Key Points:**
- Synthetic (simulated) bias **will not replace real data** — it will only be used to test the *sensitivity* and correctness of the bias detection algorithm.  
- The main validation will rely on **physical experiments** using a consumer-grade roulette wheel (≈€100) with controlled manipulations such as tilt or added weights.  
- Before purchasing, I will demonstrate feasibility using **public roulette videos** to validate the ball-tracking and homography pipeline.  
- Once the system performs reliably, the real wheel data will be used to confirm calibration accuracy and to show that the tool can detect geometric or mechanical deviations.  
- This approach keeps the project **valid, transparent, and experimentally grounded**, addressing the mentor’s concerns about credibility while retaining the original vision.

👉 See [[(1) 2025-10-24]] for the meeting summary where this topic was discussed