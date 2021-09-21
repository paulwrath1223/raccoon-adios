import cv2


import serial
import time


def write_read(message):
    if arduino_output:
        arduino.write(bytes(str(message), 'utf-8'))
        time.sleep(0.05)
        data = arduino.readline()
        return data
    return ""


def set_pos(x, y):
    out = str(x)+str(y)+"\n"
    value = write_read(out)
    print(f"write :{out}")
    print(f"read :{value}")


# ^ pip install opencv-contrib-python

# Enable camera

arduino_output = False

if arduino_output:
    arduino = serial.Serial(port='COM20', baudrate=115200, timeout=.1)  # change com port depending on the com port

resX = 1920.0  # constants for camera res (does not need to match real res)
resY = 1080.0

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, resX)
cap.set(4, resY)

# import cascade file for facial recognition
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# if you want to detect any object for example eyes, use one more layer of classifier as below:
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

dxd = 0
dyd = 0

eye_conf_threshold = 3  # const
face_conf_threshold = 3  # const


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
    eyes = eyeCascade.detectMultiScale3(
        imgGray,
        outputRejectLevels=True)
    faces = faceCascade.detectMultiScale3(
        imgGray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        outputRejectLevels=True)

    eye_coords = []
    face_coords = []
    # print(faces)
    # print(f"confidence = {eyes[2][0][0]}")
    #
    # for (x, y, w, h) in faces[0]:
    #     face_coords.append((x + (w/2), y + (h/2)))
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    for counter in range(len(eyes[2])):
        if eyes[2][counter][0] > eye_conf_threshold:
            ex, ey, ew, eh = eyes[0][counter]
            eye_coords.append((ex + (ew / 2), ey + (eh / 2)))
            img = cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 3)

    eye_in_face_coords = (-1, -1)

    for counter in range(len(faces[2])):
        if faces[2][counter][0] > face_conf_threshold:
            fx, fy, fw, fh = faces[0][counter]
            for eye_coord in eye_coords:
                currentX = eye_coord[0]
                currentY = eye_coord[1]
                if fx < currentX < fx+fw and fy < currentY < fy+fh:
                    eye_in_face_coords = (currentX, currentY)
            eye_coords.append((fx + (fw / 2), fy + (fh / 2)))
            img = cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 3)

    eyesX = []
    eyesY = []
    if eye_in_face_coords != (-1, -1):
        targetX = eye_in_face_coords[0]
        targetY = eye_in_face_coords[1]
    elif len(eye_coords) > 0:
        for eye in eye_coords:
            eyesX.append(eye[0])
            eyesY.append(eye[1])
        targetX = int(sum(eyesX) / len(eyesX))
        targetY = int(sum(eyesY) / len(eyesY))
    else:  # if no target currently on screen, do not move camera
        targetX = (resX/2)
        targetY = (resY/2)

    weightedX = int(float((resX/2) - targetX)/(resX/100))  # expected range: [-100,100]
    weightedY = int(float((resY/2) - targetY)/(resY/100))  # expected range: [-100,100]

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

    print(f"targetX: {targetX}\ntargetY: {targetY}")
    set_pos(dx, dy)
    # img = cv2.rectangle(img, (targetX-5, targetY-5), (targetX+5, targetY+5), (255, 255, 0), 3)

    cv2.imshow('face_detect', img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyWindow('face_detect')
