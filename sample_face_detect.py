import cv2

# import serial
# import time
# arduino = serial.Serial(port='COM20', baudrate=115200, timeout=.1)  # change com port depending on the com port


def write_read(message):
    # arduino.write(bytes(str(message), 'utf-8'))  # gives 'TypeError: encoding without a string argument'
    # time.sleep(0.05)
    # data = arduino.readline()
    # return data
    return ""


def set_pos(x, y):
    out = str(x)+str(y)+"\n"
    value = write_read(out)
    print(f"write :{out}")
    print(f"read :{value}")


# ^ pip install opencv-contrib-python

# Enable camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 420)

# import cascade file for facial recognition
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# if you want to detect any object for example eyes, use one more layer of classifier as below:
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

dxd = 0
dyd = 0

eye_coords = []
targetX, targetY = 0, 0
dx, dy = 0, 0
loop_counter = 0

while True:
    success, img = cap.read()
    try:
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:  # Fix pep thing Vojta
        raise Exception("Camera not found!")

    # Getting corners around the face

    # detecting eyes
    eyes = eyeCascade.detectMultiScale(imgGray)
    faces = faceCascade.detectMultiScale(
        imgGray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    # drawing bounding box for eyes

    eye_coords = []
    face_coords = []
    for (x, y, w, h) in faces:
        face_coords.append((x + (w/2), y + (h/2)))
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    for (ex, ey, ew, eh) in eyes:
        eye_coords.append((ex + (ew / 2), ey + (eh / 2)))
        img = cv2.rectangle(img, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 3)

    eyesX = []
    eyesY = []
    if len(face_coords) > 0:
        targetX = int(face_coords[0][0])
        targetY = int(face_coords[0][1])
    elif len(eye_coords) > 0:
        for eye in eye_coords:
            eyesX.append(eye[0])
            eyesY.append(eye[1])
        targetX = int(sum(eyesX) / len(eyesX))
        targetY = int(sum(eyesY) / len(eyesY))
    else:  # if no target currently on screen, do not move camera
        targetX = 320
        targetY = 210

    weightedX = int(float(320 - targetX)/3.2)  # expected range: [-100,100]
    weightedY = int(float(210 - targetY)/2.1)  # expected range: [-100,100]
    if loop_counter < 100:
        loop_counter += 1
    else:
        loop_counter = 0

    if -10 > weightedX:
        dxd = 2  # 2 means -1, but using only one char
    elif weightedX > 10:
        dxd = 1
    else:
        dxd = 0

    if -10 > weightedY:
        dyd = 1
    elif weightedY > 10:
        dyd = 2  # 2 means -1, but using only one char
    else:
        dyd = 0

    if abs(weightedX) > loop_counter:
        dx = dxd
    else:
        dx = 0
    if abs(weightedY) > loop_counter:
        dy = dyd
    else:
        dy = 0

    print(f"weightedX: {weightedX}\nweightedY: {weightedY}")

    # print(f"targetX: {targetX}\ntargetY: {targetY}")
    set_pos(dx, dy)
    img = cv2.rectangle(img, (targetX-5, targetY-5), (targetX+5, targetY+5), (255, 255, 0), 3)

    cv2.imshow('face_detect', img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyWindow('face_detect')
