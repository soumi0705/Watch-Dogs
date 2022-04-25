from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
cam = cv2.VideoCapture(0)
# cam.set(3, 640)  # set video widht
# cam.set(4, 480)  # set video height

# # Define min window size to be recognized as a face
# minW = 0.1*cam.get(3)
# minH = 0.1*cam.get(4)
app = Flask(__name__)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
test2 = faceCascade.load('haarcascade_frontalface_default.xml')
print(test2)
font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Soumitro']

# Initialize and start realtime video capture


# soumi_image = face_recognition.load_image_file("Soumitro/Soumitro.jpg")
# soumi_face_encoding = face_recognition.face_encodings(soumi_image)[0]


# # Create arrays of known face encodings and their names
# known_face_encodings = [
#     soumi_face_encoding]
# known_face_names = [
#     "Soumitro"
# ]
# # Initialize some variables
# face_locations = []
# face_encodings = []
# face_names = []
# process_this_frame = True

def gen_frames():
    while True:
        success, frame = cam.read()  # read the camera frame
        if not success:
            break
        else:
            # # Resize frame of video to 1/4 size for faster face recognition processing
            # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            # rgb_small_frame = small_frame[:, :, ::-1]

            # # Only process every other frame of video to save time

            # # Find all the faces and face encodings in the current frame of video
            # face_locations = face_recognition.face_locations(rgb_small_frame)
            # face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            # face_names = []
            # for face_encoding in face_encodings:
            #     # See if the face is a match for the known face(s)
            #     matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            #     name = "Unknown"
            #     # Or instead, use the known face with the smallest distance to the new face
            #     face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            #     best_match_index = np.argmin(face_distances)
            #     if matches[best_match_index]:
            #         name = known_face_names[best_match_index]

            #     face_names.append(name)

            # # Display the results
            # for (top, right, bottom, left), name in zip(face_locations, face_names):
            #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #     top *= 4
            #     right *= 4
            #     bottom *= 4
            #     left *= 4

            #     # Draw a box around the face
            #     cv2.rectangle(frame, (left, top), (right, bottom), (105,105,105), 2)

            #     # Draw a label with a name below the face
            #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (105,105,105), cv2.FILLED)
            #     font = cv2.FONT_HERSHEY_DUPLEX
            #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                # minSize=(int(minW), int(minH)),
            )

            for(x, y, w, h) in faces:

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match
                if (confidence < 100):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(frame, str(id), (x+5, y-5),
                            font, 1, (255, 255, 255), 2)
                cv2.putText(frame, str(confidence), (x+5, y+h-5),
                            font, 1, (255, 255, 0), 1)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    app.run(debug=True, port=5001)
