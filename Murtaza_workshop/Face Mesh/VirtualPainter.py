import cv2
import numpy as np
import os

#######################
brushThickness = 25
eraserThickness = 100
########################

folderPath = r"C:\Users\anila\OneDrive\Documents\Python_practice\Murtaza_workshop\Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Replace with a simple method to track hands, if not using HandTrackingModule
# Assuming you have a function named 'find_hands_and_landmarks' for hand detection

xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = find_hands_and_landmarks(img)  # Replace with your hand detection logic
    lmList = findPosition(img, draw=False)  # Replace with your landmark finding logic

    if len(lmList) != 0:
        # Ensure lmList has enough elements before accessing
        if len(lmList) > 12:  # Check if there are enough landmarks
            # Tip of index and middle fingers
            x1, y1 = lmList[8][1:]  # Index finger tip
            x2, y2 = lmList[12][1:]  # Middle finger tip

            # 3. Check which fingers are up
            fingers = fingersUp()  # Replace with your fingers checking logic

            # 4. If Selection Mode – Two fingers are up
            if fingers[1] and fingers[2]:  # Index and middle fingers up
                print("Selection Mode")
                # Checking for the click
                if y1 < 125:
                    if 250 < x1 < 450:
                        header = overlayList[0]
                        drawColor = (255, 0, 255)
                    elif 550 < x1 < 750:
                        header = overlayList[1]
                        drawColor = (255, 0, 0)
                    elif 800 < x1 < 950:
                        header = overlayList[2]
                        drawColor = (0, 255, 0)
                    elif 1050 < x1 < 1200:
                        header = overlayList[3]
                        drawColor = (0, 0, 0)
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

            # 5. If Drawing Mode – Index finger is up
            if fingers[1] and not fingers[2]:  # Only index finger up
                print("Drawing Mode")
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                xp, yp = x1, y1
            else:
                xp, yp = 0, 0  # Reset the previous point when fingers are not in drawing mode

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header image
    img[0:125, 0:1280] = header
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)
