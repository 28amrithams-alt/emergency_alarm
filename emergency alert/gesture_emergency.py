import cv2
import mediapipe as mp
import socket
import pygame

# ---------------------- SOCKET SETUP ----------------------
HOST = '127.0.0.1'  # receiver IP
PORT = 5050
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# ---------------------- ALARM SETUP ----------------------
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
pygame.mixer.music.load("alarm.wav")  # put alarm.wav in same folder

# ---------------------- MEDIAPIPE -------------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# ---------------------- CAMERA SETUP ----------------------
cap = cv2.VideoCapture(0)

# ---------------------- FLAGS -----------------------------
alarm_triggered = False
last_gesture = None

# ---------------------- GESTURE DETECTION -----------------
def detect_gesture(landmarks):
    """
    Returns:
    - "Normal"  -> Palm open
    - "Moderate" -> Thumb up
    - "Emergency" -> Fist
    """
    fingers = []

    # Thumb
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for tip_id, pip_id in [(8,6), (12,10), (16,14), (20,18)]:
        if landmarks[tip_id].y < landmarks[pip_id].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total_fingers = sum(fingers)

    if total_fingers >= 4:
        return "Normal"       # Palm open
    elif fingers[0] == 1 and sum(fingers[1:]) <= 1:
        return "Moderate"     # Thumb up
    elif total_fingers <= 1:
        return "Emergency"    # Fist
    else:
        return "Moderate"

# ---------------------- MAIN LOOP -------------------------
try:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Mirror the camera
        image = cv2.flip(image, 1)

        # Convert to RGB for MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = hands.process(image_rgb)
        image_rgb.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = detect_gesture(hand_landmarks.landmark)

                # Send gesture only if changed
                if gesture != last_gesture:
                    sock.sendall(gesture.upper().encode())
                    last_gesture = gesture

                # Handle gestures
                if gesture == "Normal":
                    cv2.putText(image, "Detected: Normal (Palm Open)", (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    if alarm_triggered:
                        pygame.mixer.music.stop()
                        alarm_triggered = False

                elif gesture == "Moderate":
                    cv2.putText(image, "Detected: Moderate (Thumb Up)", (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    if alarm_triggered:
                        pygame.mixer.music.stop()
                        alarm_triggered = False

                elif gesture == "Emergency":
                    cv2.putText(image, "🚨 Emergency! Fist Detected!", (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    if not alarm_triggered:
                        print("🚨 Alarm triggered! Waiting for staff...")
                        pygame.mixer.music.play(-1)  # loop until stopped
                        alarm_triggered = True

        else:
            # No hand detected
            gesture = None

        cv2.imshow('Gesture Emergency System', image)

        # Stop alarm manually by pressing any key
        key = cv2.waitKey(5)
        if key != -1 and alarm_triggered:
            pygame.mixer.music.stop()
            alarm_triggered = False

        if key == 27:  # ESC to exit
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    sock.close()
    pygame.quit()
