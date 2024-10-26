import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)

def is_finger_up(landmarks, tip_index, pip_index):
    return landmarks[tip_index].y < landmarks[pip_index].y

def get_finger_status(landmarks):
    thumb = is_finger_up(landmarks, 4, 3)  
    index = is_finger_up(landmarks, 8, 6)
    middle = is_finger_up(landmarks, 12, 10)
    ring = is_finger_up(landmarks, 16, 14)
    pinky = is_finger_up(landmarks, 20, 18)
    return [thumb, index, middle, ring, pinky]

previous_status = [0, 0, 0, 0, 0]
printing = False
printing_module_started = False

while True:
    ret, frame = video.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            current_status = get_finger_status(hand_landmarks.landmark)

            if current_status == [1, 0, 0, 0, 0] and not printing:
                if not printing_module_started:
                    print("Starting finger print module")
                    printing_module_started = True
                printing = True

            if printing and current_status != previous_status and current_status != [1, 0, 0, 0, 0]:
                print(f"Finger status (thumb to pinky): {current_status}")

            if current_status == [1, 0, 0, 0, 1] and printing:
                if printing_module_started:
                    print("Ending finger print module")
                    printing_module_started = False
                printing = False

            previous_status = current_status


    cv2.imshow("Hand Detection", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

video.release()
cv2.destroyAllWindows()
