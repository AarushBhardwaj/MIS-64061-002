import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, max_hands=4,
                 model_complexity=1, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_Hands = mp.solutions.hands
        self.hands = self.mp_Hands.Hands(self.mode, self.max_hands, self.model_complexity,
                                         self.detection_confidence, self.tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, image, draw = True):

        image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_RGB)

        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:

                if draw:
                    # To draw the points and connections on hands
                    self.mpDraw.draw_landmarks(image, hand_landmarks, self.mp_Hands.HAND_CONNECTIONS)

        return  image

    def find_position(self, image, hand_number=0, draw=True):

        landmark_list = []

        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[hand_number]

            for id, landmark in enumerate(myhand.landmark):
                h, w, c = image.shape

                cx, cy = int(landmark. x * w), int(landmark. y * h)
                #print(id, cx, cy)
                landmark_list.append([id, cx, cy])

                # Making a circle around a landmark
                if draw:
                    cv2.circle(image, (cx, cy), 7, (255, 0, 0), cv2.FILLED)

        return landmark_list



def main():
    previous_time = 0
    current_time = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, image = cap.read()
        image = detector.find_hands(image)
        landmark_list = detector.find_position(image)
        if len(landmark_list) != 0:
            print(landmark_list[4])

        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", image)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()

