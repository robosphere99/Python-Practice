import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import ctypes

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

# Function to ensure mouse cursor remains visible
def show_mouse_cursor():
    ctypes.windll.user32.ShowCursor(True)

# Make sure the pointer is visible
show_mouse_cursor()

# Get screen size
screen_width, screen_height = pyautogui.size()

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
            # Get the index finger tip coordinates
            index_finger_tip = hand_landmarks.landmark[8]
            index_x = int(index_finger_tip.x * frame_width)
            index_y = int(index_finger_tip.y * frame_height)

            # Map the finger tip's position to the screen size
            screen_x = np.interp(index_x, [0, frame_width], [0, screen_width])
            screen_y = np.interp(index_y, [0, frame_height], [0, screen_height])

            # Move the mouse cursor to that position
            pyautogui.moveTo(screen_x, screen_y)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release OpenCV resources
cap.release()
cv2.destroyAllWindows()
