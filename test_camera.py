# ═══════════════════════════════════════════════════════════════════════════════
# STANDALONE HARDWARE TEST — DO NOT RUN WHILE main.py IS ACTIVE
# Running this while JARVIS is running will cause MSMF camera conflicts.
# To check camera health while JARVIS is running, use instead:
#   python -c "from modules.camera_manager import get_instance; print(get_instance().get_health())"
# ═══════════════════════════════════════════════════════════════════════════════
import cv2
import time
import numpy as np

def wake_camera():
    print("[CAMERA] Waking up camera...")
    
    # Open and immediately release — forces init
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(1)
    cap.release()
    time.sleep(0.5)
    
    # Now open properly
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    
    # Wait for brightness to stabilize
    print("[CAMERA] Stabilizing...")
    for i in range(30):
        ret, frame = cap.read()
        if ret:
            brightness = np.mean(frame)
            print(f"Frame {i}: brightness={brightness:.1f}")
            if brightness > 20:
                print("[CAMERA] Ready!")
                return cap, frame
        time.sleep(0.1)
    
    return cap, None

cap, frame = wake_camera()

if frame is not None:
    cv2.imwrite("D:/JARVIS/test_final.jpg", frame)
    print("SUCCESS! Photo saved.")
    
    # Show live preview
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

cap.release()