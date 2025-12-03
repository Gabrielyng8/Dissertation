import cv2
import numpy as np

from utils.file_dialog_utils import pick_media_cv2

# --- 1. Video capture (change to 0 for webcam) ---
# cap = cv2.VideoCapture("wheel.mp4")
media_obj, media_path, source_kind = pick_media_cv2(title="Select a video file for HSV detection")
cap = media_obj
if source_kind != "video":
    raise ValueError("Please select a video file.")

# Rough initial guess for green in HSV
# You WILL need to tweak these for your actual footage
lower_green = np.array([40, 50, 50])   # H, S, V
upper_green = np.array([90, 255, 255])

kernel = np.ones((5, 5), np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot read frame.")
        break

    # Optional: resize for speed
    # frame = cv2.resize(frame, (960, 540))

    # --- 2. Convert to HSV ---
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --- 3. Threshold for green ---
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # --- 4. Morphological cleanup ---
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # --- 5. Find contours in the mask ---
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cx, cy = None, None

    if contours:
        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 100:   # ignore tiny blobs/noise; tune this
                continue

            # --- 6. Compute centroid using moments ---
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Draw the contour and centroid for visualization
            cv2.drawContours(frame, [cnt], -1, (255, 0, 0), 2)  # blue contour
            cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)     # red dot at centroid
            cv2.putText(frame, "ZERO", (cx + 10, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            break  # stop after first valid contour

    # --- 7. Show the original frame and mask ---
    cv2.imshow("Frame", frame)
    cv2.imshow("Green Mask", mask)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):   # ESC or q to quit
        break

cap.release()
cv2.destroyAllWindows()