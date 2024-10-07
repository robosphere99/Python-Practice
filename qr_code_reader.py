import cv2
from pyzbar.pyzbar import decode

# Function to read and decode QR code from the image
def read_qr_code(frame):
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        # Extract the bounding box coordinates and decode the QR data
        points = obj.polygon
        if len(points) == 4:
            pts = [(point.x, point.y) for point in points]
            pts = sorted(pts, key=lambda x: x[1])
            cv2.polylines(frame, [np.array(pts, np.int32)], True, (0, 255, 0), 3)
        
        qr_data = obj.data.decode('utf-8')
        print("QR Code Detected: ", qr_data)

        # Show the decoded data on the frame
        cv2.putText(frame, qr_data, (pts[0][0], pts[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return frame

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect and decode QR codes
    frame_with_qr = read_qr_code(frame)

    # Display the video feed
    cv2.imshow("QR Code Reader", frame_with_qr)

    # Exit the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
