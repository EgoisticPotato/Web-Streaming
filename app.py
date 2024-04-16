from flask import Flask,render_template,Response
import cv2

app = Flask(__name__, template_folder='Templates')
cam1=cv2.VideoCapture(0)



@app.route('/')
def Index():
    return render_template("index.html")

def Generate_Frames():
    ## Read the camera frame and give two parameters 
    while True:
        success1,frame1=cam1.read()
        if not success1:
            break
        else:
            ret1,buffer1=cv2.imencode('.jpg',frame1)
            frame1=buffer1.tobytes()
           
        
        yield(b'--frame\r\n'b'Content-Type: image/jpg\r\n\r\n'+frame1+
              b'\r\n')

@app.route('/video')
def video():
    return Response(Generate_Frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
