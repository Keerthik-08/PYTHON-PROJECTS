import cv2

# Load face detector
face_cap = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Load gender model
gender_model = cv2.dnn.readNet(
    "models/gender_net.caffemodel",
    "models/gender_deploy.prototxt"
)

# Gender labels
gender_list = ['Male', 'Female']

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

        # Convert face to blob
        blob = cv2.dnn.blobFromImage(
            face,
            1.0,
            (227, 227),
            (78.4263377603, 87.7689143744, 114.895847746),
            swapRB=False
        )

        # Predict gender
        gender_model.setInput(blob)
        gender_preds = gender_model.forward()

        gender = gender_list[gender_preds[0].argmax()]

        # Draw rectangle
        cv2.rectangle(video_data, (x, y), (x+w, y+h), (0,255,0), 2)

        # Show gender
        cv2.putText(
            video_data,
            f"Gender: {gender}",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    cv2.imshow("Gender Detection Project", video_data)

    # Press a to exit
    if cv2.waitKey(10) == ord("a"):
        break

video_cap.release()
cv2.destroyAllWindows()