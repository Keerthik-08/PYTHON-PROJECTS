import cv2

# Load the face detection model
face_cap = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Start webcam
video_cap = cv2.VideoCapture(0)

while True:
    ret, video_data = video_cap.read()

    # Convert video to grayscale
    col = cv2.cvtColor(video_data, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cap.detectMultiScale(
        col,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw rectangle around face
    for (x, y, w, h) in faces:
        cv2.rectangle(video_data, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Show webcam window
    cv2.imshow("Face Detection Project", video_data)

    # Press 'a' to exit
    if cv2.waitKey(10) == ord("a"):
        break

# Close webcam
video_cap.release()
cv2.destroyAllWindows()