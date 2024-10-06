import cv2
import mediapipe as mp
import numpy as np
from math import degrees, acos

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to calculate the angle between three points (P1, P2, P3)
def calculate_angle(P1, P2, P3):
    a = np.array([P1.x, P1.y])  # First point
    b = np.array([P2.x, P2.y])  # Midpoint
    c = np.array([P3.x, P3.y])  # Endpoint
    
    # Calculate the angle using dot product and magnitude
    radians = np.arccos(np.dot(a-b, c-b) / (np.linalg.norm(a-b) * np.linalg.norm(c-b)))
    angle = np.degrees(radians)
    
    return angle

# Initialize webcam feed
cap = cv2.VideoCapture(0)

# Set up the pose estimation model
with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Flip the frame horizontally and convert to RGB for processing
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame to detect body pose
        results = pose.process(rgb_frame)

        # Convert the frame back to BGR for OpenCV rendering
        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        # Draw pose landmarks and connections
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Extract specific landmarks
            landmarks = results.pose_landmarks.landmark

            # Example: Checking angles for posture detection
            # Left side joints
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

            # Calculate angle at the left elbow
            elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

            # Right side joints (for squats or posture tracking)
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
            right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

            # Calculate knee angle (important for squat form)
            knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

            # Visualize the angles on the frame
            cv2.putText(frame, f'Elbow Angle: {int(elbow_angle)}', (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f'Knee Angle: {int(knee_angle)}', (50, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Posture classification based on angles
            if elbow_angle > 160:
                cv2.putText(frame, "Arm Extended", (50, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Arm Bent", (50, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Check squat form based on knee angle
            if knee_angle < 90:
                cv2.putText(frame, "Squat: Low", (50, 200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Squat: High", (50, 200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the frame with posture detection
        cv2.imshow('Advanced Body Posture Tracking', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
