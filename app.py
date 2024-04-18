from flask import Flask, render_template, Response
import cv2

app = Flask(__name__, template_folder='Templates')

def generate_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video')
def video_feed():
    camera = cv2.VideoCapture(0)  # Use the correct camera index (0 or 1 depending on your setup)
    return Response(generate_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
