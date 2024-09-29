import cv2
import numpy as np
import face_recognition
import csv
import win32com.client as wincl
import time
from datetime import datetime

v_capture = cv2.VideoCapture(0)

student1 = face_recognition.load_image_file("Data/student1.jpg")
student1_encoding = face_recognition.face_encodings(student1)[0]
student2 = face_recognition.load_image_file("Data/student2.jpg")
student2_encoding = face_recognition.face_encodings(student2)[0]
student3 = face_recognition.load_image_file("Data/student3.jpg")
student3_encoding = face_recognition.face_encodings(student3)[0]
student4 = face_recognition.load_image_file("Data/student4.jpg")
student4_encoding = face_recognition.face_encodings(student4)[0]

student_face_encoding = [student1_encoding, student2_encoding, student3_encoding, student4_encoding]
student_name = ["student1", "student2", "student3", "student4"]

#Expected students
students = student_name.copy()

acknowledged_students = set()
no_face_timer = 0
max_no_face_time = 500

face_locations = []
face_encodings = []

#Current date and time
now = datetime.now()
current_date = now.strftime("%d- %m -%y")

f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)

while True:
    ret, frame = v_capture.read()
    if not ret:
        break
    small_frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    
    #Face recognization

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        matches = face_recognition.compare_faces(student_face_encoding, face_encoding)

        #Finds the similarity between the known faces and the face detected by webcam.
        
        face_distance = face_recognition.face_distance(student_face_encoding, face_encoding)
        best_match = np.argmin(face_distance)

        #Returning the name of the student with whom the face has matched
        if(matches[best_match]):
            name = student_name[best_match]
            current_time = now.strftime("%H-%M-%S")
            lnwriter.writerow([name, current_time])  # Add to the set

        if name in student_name:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomleft = (10, 100)
            fontScale = 1.5
            fontColor = (255, 0, 0)
            thickness = 3
            linetype = 2

            cv2.putText(frame, name + "Present", bottomleft, font, fontScale, fontColor, thickness, linetype)
    cv2.imshow("Attendace", frame)

    if name not in acknowledged_students:  # Check if not acknowledged
                a = f"{name} is present"
                speak = wincl.Dispatch("SAPI.SpVoice")
                speak.Speak(a)
                acknowledged_students.add(name)
    if not face_encodings:  # No faces detected
            no_face_timer += 1  # Increment the timer (assuming the loop runs every second)
    else:
            no_face_timer = 0  # Reset timer if a face is detected

        # Check if no face has been detected for too long
    if no_face_timer > max_no_face_time:
            print("No face detected. Closing application.")
            break  # Exit the loop if no face detected for too long
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
v_capture.release()
cv2.destroyAllWindows()
f.close