import cv2

# ^ pip install opencv-contrib-python

# TODO: empty 'face_coords' if no face has been detecting for a couple seconds

# Enable camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 420)

# import cascade file for facial recognition
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# if you want to detect any object for example eyes, use one more layer of classifier as below:
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

face_coords = []

while True:
    success, img = cap.read()
    try:
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        raise Exception("Camera not found!")

    # Getting corners around the face
    faces = faceCascade.detectMultiScale(imgGray, 1.3, 5)  # 1.3 = scale factor, 5 = minimum neighbor
    # drawing bounding box around face
    if len(faces) != 0:
        face_coords = []  # list of tuples containing coordinates of the center of the face
    for (x, y, w, h) in faces:
        face_coords.append((x+(w/2), y+(h/2)))
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # detecting eyes
    eyes = eyeCascade.detectMultiScale(imgGray)
    # drawing bounding box for eyes
    for (ex, ey, ew, eh) in eyes:
        img = cv2.rectangle(img, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 3)

    cv2.imshow('face_detect', img)
    print(face_coords)  # prints last known coords of face
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyWindow('face_detect')
