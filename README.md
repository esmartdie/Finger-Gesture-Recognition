# Project: Real-Time Finger Gesture Recognition

This project implements a real-time hand gesture recognition system using **MediaPipe** and **OpenCV** in Python. The program detects hand landmarks and interprets the status of each finger (up or down) based on the position of key points. By recognizing specific gestures, the program can trigger different actions, such as starting or stopping a "printing module" based on finger movements.

## Technologies and Libraries

- **Python**: The primary programming language used for real-time processing and gesture recognition.
- **OpenCV**: A library for computer vision tasks, used to capture and display video frames in real-time.
- **MediaPipe**: A library by Google for high-fidelity hand tracking and landmark detection, used here to detect and analyze hand movements.
- **Math**: Used to calculate distances between hand landmarks.

## Key Features

- **Real-Time Finger Detection**: The program captures video frames, processes them in real-time, and identifies the status (up or down) of each finger.
- **Gesture Recognition**:
  - Activates a "printing module" when the thumb is raised.
  - Prints the status of each finger (thumb to pinky) when the hand’s gesture changes.
  - Deactivates the "printing module" when both the thumb and pinky are raised.
- **Visual Feedback**: Shows a window with real-time detection of hand landmarks and finger connections.

## Code Review


1. Initialize MediaPipe Hands:
   
   ```
   mp_hands = mp.solutions.hands
   hands = mp_hands.Hands(
       max_num_hands=1,
       min_detection_confidence=0.7,
       min_tracking_confidence=0.7
   )
   ```


3. OpenCV Video Capture

   
```
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```
Starts capturing video from the default camera, setting the frame dimensions to 640x480.

4. Finger Status Evaluation:
   
```
def is_finger_up(landmarks, tip_index, pip_index):
    return landmarks[tip_index].y < landmarks[pip_index].y

```
This function evaluates whether a finger is up based on the y-coordinates of the tip and middle joint landmarks.

5. Gesture Recognition:
```
def get_finger_status(landmarks):
    thumb = is_finger_up(landmarks, 4, 3)
    index = is_finger_up(landmarks, 8, 6)
    middle = is_finger_up(landmarks, 12, 10)
    ring = is_finger_up(landmarks, 16, 14)
    pinky = is_finger_up(landmarks, 20, 18)
    return [thumb, index, middle, ring, pinky]
```
Determines the status of each finger by checking if specific landmarks are above their previous joint landmarks.


Gesture-Based Module Control
</br>The loop continuously checks for gestures and activates or deactivates the "printing module" based on specific finger configurations:

Activate Printing Module: The program checks if only the thumb is raised and starts the printing module.

```
if current_status == [1, 0, 0, 0, 0] and not printing:
    if not printing_module_started:
        print("Starting finger print module")
        printing_module_started = True
    printing = True
```
Print Finger Status: While the printing module is active, it prints the status of each finger whenever the gesture changes.

```
if printing and current_status != previous_status and current_status != [1, 0, 0, 0, 0]:
    print(f"Finger status (thumb to pinky): {current_status}")
```
Deactivate Printing Module: If both the thumb and pinky are raised, the program ends the printing module.

```
if current_status == [1, 0, 0, 0, 1] and printing:
    if printing_module_started:
        print("Ending finger print module")
        printing_module_started = False
    printing = False
```


## Summary
This project showcases a simple yet effective real-time gesture recognition system using MediaPipe and OpenCV. The use of specific gestures to control a "printing module" demonstrates the potential for gesture-based interfaces in various applications.
