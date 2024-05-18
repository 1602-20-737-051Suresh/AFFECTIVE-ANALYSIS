### General imports ###
from __future__ import division

import numpy as np
# import pandas as pd
import cv2

from time import time
from time import sleep
# import re
# import os

# import argparse
# from collections import OrderedDict

from scipy.ndimage import zoom
from scipy.spatial import distance
# import imutils
# from scipy import ndimage

import dlib

from tensorflow.keras.models import load_model
from imutils import face_utils

# import requests

global shape_x
global shape_y
global input_shape
global nClasses

def show_webcam() :

    shape_x = 48
    shape_y = 48
    # input_shape = (shape_x, shape_y, 1)
    # nClasses = 7

    # thresh = 0.25
    # frame_check = 20

    # def eye_aspect_ratio(eye):
    #     A = distance.euclidean(eye[1], eye[5])
    #     B = distance.euclidean(eye[2], eye[4])
    #     C = distance.euclidean(eye[0], eye[3])
    #     ear = (A + B) / (2.0 * C)
    #     return ear

    # (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    # (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    
    # (nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
    # (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    # (jStart, jEnd) = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]

    # (eblStart, eblEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
    # (ebrStart, ebrEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]

    model = load_model('Models/video.h5',compile=False)
    face_detect = dlib.get_frontal_face_detector()
    predictor_landmarks  = dlib.shape_predictor("Models/face_landmarks.dat")
    
    #Lancer la capture video
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        # face_index = 0
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = face_detect(gray, 1)
        #gray, detected_faces, coord = detect_face(frame)

        for (i, rect) in enumerate(rects):

            shape = predictor_landmarks(gray, rect)
            shape = face_utils.shape_to_np(shape)
            
            # Identify face coordinates
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            face = gray[y:y+h,x:x+w]
            
            #Zoom on extracted face
            face = zoom(face, (shape_x / face.shape[0],shape_y / face.shape[1]))
            
            #Cast type float
            face = face.astype(np.float32)
            
            #Scale
            face /= float(face.max())
            face = np.reshape(face.flatten(), (1, 48, 48, 1))
            
            #Make Prediction
            prediction = model.predict(face)
            prediction_result = np.argmax(prediction)
            
            # Rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
            cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
     
            for (j, k) in shape:
                cv2.circle(frame, (j, k), 1, (0, 0, 255), -1)
            
            # 1. Add prediction probabilities
            cv2.putText(frame, "----------------",(40,100 + 180*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
            cv2.putText(frame, "Emotional report : Face #" + str(i+1),(40,120 + 180*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
            cv2.putText(frame, "Angry : " + str(round(prediction[0][0],3)),(40,140 + 180*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
            cv2.putText(frame, "Disgust : " + str(round(prediction[0][1],3)),(40,160 + 180*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 0)
            cv2.putText(frame, "Fear : " + str(round(prediction[0][2],3)),(40,180 + 180*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
            cv2.putText(frame, "Happy : " + str(round(prediction[0][3],3)),(40,200 + 180*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
            cv2.putText(frame, "Sad : " + str(round(prediction[0][4],3)),(40,220 + 180*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
            cv2.putText(frame, "Surprise : " + str(round(prediction[0][5],3)),(40,240 + 180*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
            cv2.putText(frame, "Neutral : " + str(round(prediction[0][6],3)),(40,260 + 180*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 155, 1)
            
            # 2. Annotate main image with a label
            if prediction_result == 0 :
                cv2.putText(frame, "Angry",(x+w-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif prediction_result == 1 :
                cv2.putText(frame, "Disgust",(x+w-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif prediction_result == 2 :
                cv2.putText(frame, "Fear",(x+w-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif prediction_result == 3 :
                cv2.putText(frame, "Happy",(x+w-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif prediction_result == 4 :
                cv2.putText(frame, "Sad",(x+w-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif prediction_result == 5 :
                cv2.putText(frame, "Surprise",(x+w-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else :
                cv2.putText(frame, "Neutral",(x+w-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 3. Eye Detection and Blink Count
            # leftEye = shape[lStart:lEnd]
            # rightEye = shape[rStart:rEnd]
            
            # Compute Eye Aspect Ratio
            # leftEAR = eye_aspect_ratio(leftEye)
            # rightEAR = eye_aspect_ratio(rightEye)
            # ear = (leftEAR + rightEAR) / 2.0
            
            # And plot its contours
            # leftEyeHull = cv2.convexHull(leftEye)
            # rightEyeHull = cv2.convexHull(rightEye)
            #cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            #cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            
            # 4. Detect Nose
            # nose = shape[nStart:nEnd]
            # noseHull = cv2.convexHull(nose)
            #cv2.drawContours(frame, [noseHull], -1, (0, 255, 0), 1)

            # 5. Detect Mouth
            # mouth = shape[mStart:mEnd]
            # mouthHull = cv2.convexHull(mouth)
            #cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
            
            # 6. Detect Jaw
            # jaw = shape[jStart:jEnd]
            # jawHull = cv2.convexHull(jaw)
            #cv2.drawContours(frame, [jawHull], -1, (0, 255, 0), 1)
            
            # 7. Detect Eyebrows
            # ebr = shape[ebrStart:ebrEnd]
            # ebrHull = cv2.convexHull(ebr)
            #cv2.drawContours(frame, [ebrHull], -1, (0, 255, 0), 1)
            # ebl = shape[eblStart:eblEnd]
            # eblHull = cv2.convexHull(ebl)
            #cv2.drawContours(frame, [eblHull], -1, (0, 255, 0), 1)
        
        cv2.putText(frame,'Number of Faces : ' + str(len(rects)),(40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, 155, 1)
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) <1:
            break

    video_capture.release()
    cv2.destroyAllWindows()

def main():
    show_webcam()

if __name__ == "__main__":
    main()
