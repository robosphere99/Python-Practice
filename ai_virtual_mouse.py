import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

# Variables for click control
click_down = False
right_click_hold = False
right_click_start_time = None

# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame for mirror effect
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get landmarks for the index, middle fingers
            index_finger_tip = hand_landmarks.landmark[8]  # Index finger tip
            middle_finger_tip = hand_landmarks.landmark[12]  # Middle finger tip

            # Get x, y coordinates of index and middle fingers
            index_x, index_y = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)
            middle_x, middle_y = int(middle_finger_tip.x * frame_width), int(middle_finger_tip.y * frame_height)

            # Calculate the screen coordinates of the index finger
            screen_x = np.interp(index_x, [0, frame_width], [0, pyautogui.size().width])
            screen_y = np.interp(index_y, [0, frame_height], [0, pyautogui.size().height])

            # Move the mouse cursor to the index finger's position
            pyautogui.moveTo(screen_x, screen_y)

            # Calculate the distance between the index and middle fingers
            finger_distance = calculate_distance(index_finger_tip, middle_finger_tip)

            # LEFT CLICK: If index and middle fingers come close together, perform a left click
            if finger_distance < 0.05 and not click_down:
                # Calculate midpoint of the index and middle fingers
                mid_x = (index_x + middle_x) // 2
                mid_y = (index_y + middle_y) // 2
                # Perform left click at midpoint
                pyautogui.click(mid_x, mid_y)
                click_down = True
            elif finger_distance >= 0.05:
                click_down = False

            # RIGHT CLICK: If the index finger stays in one position for more than 2 seconds, perform right-click
            if finger_distance > 0.2:  # Ensure only index finger is raised
                if right_click_start_time is None:
                    right_click_start_time = time.time()  # Start timer
                elif time.time() - right_click_start_time > 2:
                    pyautogui.rightClick()
                    right_click_start_time = None  # Reset timer after right-click
            else:
                right_click_start_time = None  # Reset if movement occurs

    # Exit the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release OpenCV resources
cap.release()
cv2.destroyAllWindows()
