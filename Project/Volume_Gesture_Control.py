import cv2
import time
import numpy as np
import Hand_Tracking_Module as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#volume.GetMute()
#volume.GetMasterVolumeLevel()
volume_range = volume.GetVolumeRange()
min_vol = volume_range[0]
max_vol = volume_range[1]

vol_bar = 400
vol = 0
vol_percentage = 0


# height and width of the screen
width_cam = 640
height_cam = 480

capture = cv2.VideoCapture(0)
capture.set(3, width_cam)
capture.set(4, height_cam)

previous_time = 0

detector = htm.handDetector(detection_confidence=0.7)
while True:

    success, image = capture.read()
    image = detector.find_hands(image)
    landmark_list = detector.find_position(image, draw=False)

    if len(landmark_list) != 0:
        print(landmark_list[4], landmark_list[8])

        x1, y1 = landmark_list[4][1], landmark_list[4][2]
        x2, y2 = landmark_list[8][1], landmark_list[8][2]
        # Center of the line
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(image, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(image, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.circle(image, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [50, 250], [min_vol, max_vol])
        vol_bar = np.interp(length, [50, 300], [400, 150])
        vol_percentage = np.interp(length, [50, 300], [0, 100])



        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(image, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(image, (50,150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(image, (50,int(vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, f'{int(vol_percentage)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)




    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    cv2.putText(image, f'FPS: {int(fps)}', (40, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Image", image)
    cv2.waitKey(1)
