import cv2
import numpy as np
import face_recognition
import csv
from datetime import datetime

v_capture = cv2.VideoCapture(0)

student1 = face_recognition.load_image_file("Data/student1.jpg")
student1_encoding = face_recognition.face_encodings[0]
student2 = face_recognition.load_image_file("Data/student2.jpg")
student2_encoding = face_recognition.face_encodings[0]
student3 = face_recognition.load_image_file("Data/student3.jpg")
student3_encoding = face_recognition.face_encodings[0]
student4 = face_recognition.load_image_file("Data/student4.jpg")
student4_encoding = face_recognition.face_encodings[0]

face_encoding = [student1_encoding, student2_encoding, student3_encoding, student4_encoding]
student_name = ["Student 1", "Student 2", "Student 3", "Student 4"]

students = student_name.copy()

face_locations = []
face_encodings = []

now = datetime.now()
current_date = now.strftime("%D/%M/%Y")

f = open(f"{current_date}.csv", "w+", newline=" ")
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)