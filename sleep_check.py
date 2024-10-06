import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Face and Eye model
mp_face = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Constants
EYE_CLOSED_THRESHOLD = 0.25  # Aspect ratio threshold for closed eyes
SLEEP_DURATION = 3  # Duration in seconds to consider as sleeping
sleep_count = 0
sleep_start_time = None

# Function to calculate eye aspect ratio
def eye_aspect_ratio(eye):
    # Calculate distances
    A = ((eye[1].y - eye[5].y) ** 2 + (eye[1].x - eye[5].x) ** 2) ** 0.5  # Vertical distance
    B = ((eye[2].y - eye[4].y) ** 2 + (eye[2].x - eye[4].x) ** 2) ** 0.5  # Vertical distance
    C = ((eye[0].y - eye[3].y) ** 2 + (eye[0].x - eye[3].x) ** 2) ** 0.5  # Horizontal distance
    
    # Calculate Eye Aspect Ratio (EAR)
    ear = (A + B) / (2.0 * C)
    return ear

# Initialize webcam feed
cap = cv2.VideoCapture(0)

# Set up the face mesh model
with mp_face.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7) as face_mesh:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Flip the frame horizontally and convert to RGB for processing
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame to detect faces
        results = face_mesh.process(rgb_frame)

        # Convert the frame back to BGR for OpenCV rendering
        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        # Draw landmarks and check for closed eyes
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Use FACEMESH_TESSELATION instead of FACE_CONNECTIONS
                mp_drawing.draw_landmarks(frame, face_landmarks, mp_face.FACEMESH_TESSELATION)

                # Get eye landmarks
                left_eye = [face_landmarks.landmark[i] for i in [362, 385, 386, 374, 373, 380]]
                right_eye = [face_landmarks.landmark[i] for i in [263, 390, 391, 379, 378, 385]]

                # Calculate eye aspect ratio for both eyes
                left_ear = eye_aspect_ratio(left_eye)
                right_ear = eye_aspect_ratio(right_eye)

                # Average EAR
                avg_ear = (left_ear + right_ear) / 2.0

                # Debugging: print the EAR values
                print(f"Left EAR: {left_ear:.3f}, Right EAR: {right_ear:.3f}, Average EAR: {avg_ear:.3f}")

                # Check if eyes are closed
                if avg_ear < EYE_CLOSED_THRESHOLD:
                    if sleep_start_time is None:
                        sleep_start_time = time.time()
                    else:
                        if time.time() - sleep_start_time >= SLEEP_DURATION:
                            sleep_count += 1
                            cv2.putText(frame, "Sleeping!", (50, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                else:
                    sleep_start_time = None  # Reset if eyes are open

                # Display current sleep count
                cv2.putText(frame, f'Sleep Count: {sleep_count}', (50, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Display the frame
        cv2.imshow('Sleep Detection', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
