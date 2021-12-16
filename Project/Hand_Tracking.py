import cv2
import mediapipe as mp
import time

# Capturing the webcam image and making sure that we are able to capture the image.

cap = cv2.VideoCapture(0)

mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()

mpDraw = mp.solutions.drawing_utils

previous_time = 0
current_time = 0

while True:
    success , image = cap.read()

    image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_RGB)

    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, landmark in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape

                cx, cy = int(landmark. x * w), int(landmark. y * h)
                print(id, cx, cy)

                # Making a circle around a landmark
                if id == 0:
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)

            # To draw the points and connections on hands
            mpDraw.draw_landmarks(image, hand_landmarks, mp_Hands.HAND_CONNECTIONS)

    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    cv2.putText(image, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", image)
    cv2.waitKey(1)


# Hand Detection Module

