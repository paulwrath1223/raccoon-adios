import cv2

# ^ pip install opencv-contrib-python



# Enable camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 420)

# import cascade file for facial recognition
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# if you want to detect any object for example eyes, use one more layer of classifier as below:
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")


eye_coords = []
targetX, targetY = 0, 0


while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Getting corners around the face


    # detecting eyes
    eyes = eyeCascade.detectMultiScale(imgGray)
    # drawing bounding box for eyes

    eye_coords = []
    for (ex, ey, ew, eh) in eyes:
        eye_coords.append((ex + (ew / 2), ey + (eh / 2)))
        img = cv2.rectangle(img, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 3)

    eyesX = []
    eyesY = []
    if len(eye_coords) > 0:
        for eye in eye_coords:
            eyesX.append(eye[0])
            eyesY.append(eye[1])
        targetX = int(sum(eyesX) / len(eyesX))
        targetY = int(sum(eyesY) / len(eyesY))
    if targetX < 300:
        print("left")
    elif targetX > 340:
        print("right")
    print(f"targetX: {targetX}\ntargetY: {targetY}")

    img = cv2.rectangle(img, (targetX-5, targetY-5), (targetX+5, targetY+5), (255, 255, 0), 3)

    cv2.imshow('face_detect', img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyWindow('face_detect')
