import cv2
import numpy as np
import mediapipe as mp
import random

# Initialize Mediapipe Hands for finger tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

# Initialize Snake Game parameters
frame_width, frame_height = 640, 480
snake_pos = [[100, 50]]
snake_direction = (10, 0)  # Initial direction
snake_length = 1
food_pos = [random.randint(20, frame_width - 20), random.randint(20, frame_height - 20)]
food_spawn = True
score = 0

# OpenCV video capture
cap = cv2.VideoCapture(0)
cap.set(3, frame_width)
cap.set(4, frame_height)

# Colors
food_color = (0, 255, 0)
snake_color = (255, 0, 0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame to make it mirror-like
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    # Hand Detection
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get coordinates of the forefinger tip
            finger_tip_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame_width)
            finger_tip_y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame_height)
            
            # Update snake direction based on finger position
            if abs(finger_tip_x - snake_pos[0][0]) > abs(finger_tip_y - snake_pos[0][1]):
                if finger_tip_x > snake_pos[0][0]:
                    snake_direction = (10, 0)  # Move Right
                else:
                    snake_direction = (-10, 0)  # Move Left
            else:
                if finger_tip_y > snake_pos[0][1]:
                    snake_direction = (0, 10)  # Move Down
                else:
                    snake_direction = (0, -10)  # Move Up

    # Move the snake
    new_head = [snake_pos[0][0] + snake_direction[0], snake_pos[0][1] + snake_direction[1]]
    snake_pos = [new_head] + snake_pos[:snake_length - 1]

    # Check for collisions with food
    if abs(new_head[0] - food_pos[0]) < 15 and abs(new_head[1] - food_pos[1]) < 15:
        score += 1
        snake_length += 1
        food_spawn = False

    # Respawn food
    if not food_spawn:
        food_pos = [random.randint(20, frame_width - 20), random.randint(20, frame_height - 20)]
        food_spawn = True

    # Check if the snake hits the wall or itself
    if new_head[0] < 0 or new_head[0] > frame_width or new_head[1] < 0 or new_head[1] > frame_height or new_head in snake_pos[1:]:
        print("Game Over!")
        print("Your Score:", score)
        break

    # Drawing
    cv2.rectangle(frame, (food_pos[0] - 5, food_pos[1] - 5), (food_pos[0] + 5, food_pos[1] + 5), food_color, -1)  # Draw food
    for pos in snake_pos:
        cv2.rectangle(frame, (pos[0], pos[1]), (pos[0] + 10, pos[1] + 10), snake_color, -1)  # Draw snake
    
    # Display score
    cv2.putText(frame, f'Score: {score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show frame
    cv2.imshow("Snake Game", frame)
    
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
