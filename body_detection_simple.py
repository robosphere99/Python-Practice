import cv2
import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

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

        # Process the frame to detect the body pose
        results = pose.process(rgb_frame)

        # Convert the frame back to BGR for OpenCV rendering
        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        # Draw pose landmarks and connections
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Example: Access specific body landmarks (e.g., left shoulder, right hip)
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

            # Extract x and y coordinates
            left_shoulder_coords = (int(left_shoulder.x * frame.shape[1]), int(left_shoulder.y * frame.shape[0]))
            right_hip_coords = (int(right_hip.x * frame.shape[1]), int(right_hip.y * frame.shape[0]))

            # Example of drawing circles on specific landmarks
            cv2.circle(frame, left_shoulder_coords, 10, (255, 0, 0), -1)
            cv2.circle(frame, right_hip_coords, 10, (0, 255, 0), -1)

            # Example posture detection: Checking if shoulders and hips are aligned
            if abs(left_shoulder.y - right_hip.y) < 0.05:  # Simple posture check
                cv2.putText(frame, "Good Posture", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Bad Posture", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the frame with pose landmarks
        cv2.imshow('Body Pose Tracking', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
