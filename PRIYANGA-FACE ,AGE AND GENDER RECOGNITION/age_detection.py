import cv2

# Load face detector
face_cap = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Load age model
age_model = cv2.dnn.readNet(
    "models/age_net.caffemodel",
    "models/age_deploy.prototxt"
)

# Age ranges
age_list = [
    '(0-2)', '(4-6)', '(8-12)', '(15-20)',
    '(25-32)', '(38-43)', '(48-53)', '(60-100)'
]

# Start webcam
video_cap = cv2.VideoCapture(0)

while True:
    ret, video_data = video_cap.read()

    gray = cv2.cvtColor(video_data, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cap.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:

        face = video_data[y:y+h, x:x+w]

        # Convert face into blob
        blob = cv2.dnn.blobFromImage(
            face,
            1.0,
            (227, 227),
            (78.4263377603, 87.7689143744, 114.895847746),
            swapRB=False
        )

        # Predict age
        age_model.setInput(blob)
        age_preds = age_model.forward()

        age = age_list[age_preds[0].argmax()]

        # Draw rectangle
        cv2.rectangle(video_data, (x, y), (x+w, y+h), (0,255,0), 2)

        # Display age
        cv2.putText(
            video_data,
            f"Age: {age}",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    # Show webcam
    cv2.imshow("Age Detection Project", video_data)

    # Press a to exit
    if cv2.waitKey(10) == ord("a"):
        break

video_cap.release()
cv2.destroyAllWindows()