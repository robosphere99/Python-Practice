import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Function to check if an "O" is drawn using the right hand
def is_o_drawn(right_hand_landmarks):
    # Check tips of the index and middle fingers of the right hand
    index_tip = right_hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = right_hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # Calculate the distance between the index and middle finger tips
    distance = ((index_tip.x - middle_tip.x) ** 2 + (index_tip.y - middle_tip.y) ** 2) ** 0.5

    return distance < 0.05  # Adjust threshold as needed for the "O" shape

# Function to check if the left hand is raised
def is_left_hand_raised(left_hand_landmarks):
    left_wrist = left_hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    return left_wrist.y < 0.5  # Check if wrist is above the center of the frame

# Initialize webcam feed
cap = cv2.VideoCapture(0)

# Set up the hand tracking model
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Flip the frame horizontally and convert to RGB for processing
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame to detect hands
        results = hands.process(rgb_frame)

        # Convert the frame back to BGR for OpenCV rendering
        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        # Draw hand landmarks and check for gestures
        left_hand_detected = False
        right_hand_detected = False
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if hand_landmarks:
                    hand_type = "Left" if hand_landmarks == results.multi_hand_landmarks[0] else "Right"
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    if hand_type == "Left":
                        left_hand_detected = True
                        if is_left_hand_raised(hand_landmarks):
                            current_time = datetime.now().strftime('%H:%M:%S')
                            cv2.putText(frame, f'Time: {current_time}', (50, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                    
                    if hand_type == "Right":
                        right_hand_detected = True
                        if is_o_drawn(hand_landmarks):
                            cv2.putText(frame, 'Shock!', (50, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        # Provide feedback if no hands are detected
        if not left_hand_detected and not right_hand_detected:
            cv2.putText(frame, 'No Hands Detected', (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

        # Display the frame
        cv2.imshow('Gesture-Based Time Display', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
