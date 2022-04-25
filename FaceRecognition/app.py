from flask import Flask, render_template, Response
import cv2
import numpy as np

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

app = Flask(__name__)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
test2 = faceCascade.load('haarcascade_frontalface_default.xml')
print(test2)
font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Soumitro']


def gen_frames():
    while True:
        success, img = cam.read()  # read the camera frame
        if not success:
            break
        else:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for(x, y, w, h) in faces:

                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match
                if (confidence < 100):
                    id = names[id]
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                try:
                    cv2.rectangle(img, (x, y), (x+w, y+h),
                                  (0, 255, 0), 2)
                    cv2.putText(img, str(id), (x+5, y-5),
                                font, 1, (255, 255, 255), 2)
                    cv2.putText(img, str(confidence), (x+5, y+h-5),
                                font, 1, (255, 255, 0), 1)
                except:
                    pass
            ret, buffer = cv2.imencode('.jpg', img)
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
