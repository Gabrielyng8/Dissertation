#### **Summary of Committee Feedback**

In July, I received formal feedback on my initial **Statement of Intent (SOI)**. The committee’s overall decision was _“Significant Topic Development Recommended.”_

Their main concern was that the proposed project might be **too trivial** — noting that methods for detecting bias in games of chance are already defined by regulation, and that obtaining roulette outcomes is straightforward since the wheel displays numerical pockets. They advised me to spend the summer refining or possibly re-scoping the idea, exploring alternative approaches, and preparing a clearer research direction ahead of formal mentoring in October.

---

#### **My Reflection**

I believe the committee’s interpretation of my initial SOI overlooked the **technical depth** of what I intended to achieve. The goal was never to simply “record outcomes,” but to **automate** the full visual and analytical process of assessing roulette fairness — something not covered by existing regulations, which focus solely on _electronic_ random number generators (RNGs).

After reviewing their comments, I realized that I needed to emphasize the _non-trivial aspects_ of implementation — especially the machine-learning and computer-vision challenges involved — and clarify that this is a **feasibility and proof-of-concept study**, not just a statistical exercise.

---

#### **SOI Modifications and Enhancements**

Over the summer, I significantly revised my SOI to highlight the **technical complexity** and **research contribution** of the work. The main changes were:

1. **Computer Vision for Ball Detection**
    - Clarified that the system will use **object detection models (e.g., YOLO or similar)** to detect and track the roulette ball across video frames.
    - Emphasized that this requires experimentation with detection architectures, frame pre-processing, and motion analysis — particularly since the ball is small, fast, and often blurred.
        
2. **Pocket Value Identification Layer**
    - Added an explicit **OCR component** (or alternative homography mapping technique) to determine the **landing pocket’s value** automatically.
    - Explained that this step is non-trivial because camera angles, reflections, and wheel motion complicate number recognition, and may require geometric calibration and segmentation.
        
3. **Statistical Analysis and Synthetic Bias Injection**
    - Detailed how collected results will undergo **statistical fairness testing** (e.g., Chi-square and independence tests) to evaluate randomness.
    - Acknowledged the challenge of obtaining sufficiently large real-world datasets and proposed using **artificially biased data** to simulate non-randomness, thereby validating the sensitivity of the statistical layer.
        

---

#### **Outcome and Next Steps**

After these revisions, my updated SOI now demonstrates:

- A **multi-layered technical system** combining computer vision, OCR/geometric mapping, and statistical analysis.
- A focus on **feasibility testing** rather than full casino-scale evaluation.
- Clear justification for **academic significance**, bridging computer vision research and applied statistical validation in gaming regulation.

Moving into third year, my immediate next step is to meet with my assigned mentor, present both the **OCR** and **homography-based** pocket detection approaches, and confirm which is more feasible for implementation within the dissertation timeframe.