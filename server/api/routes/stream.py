from flask import Response, Blueprint,render_template_string
import cv2, time

stream_bp = Blueprint('stream', __name__)

@stream_bp.route('/stream', methods=['GET'])
def stream():
    print("Stream request")
    def generate():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        fps = 30.0  # FPS deseados
        frame_time = 1.0 / fps  # Tiempo entre frames

        while True:
            start_time = time.time()  # Tiempo de inicio del frame

            ret, frame = cap.read()
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame = jpeg.tobytes()
            try:
                print("Yielding frame")
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n'
                       b'Content-Length: ' + bytes(str(len(frame)), 'utf-8') + b'\r\n\r\n' +
                       frame + b'\r\n\r\n')
            except:
                print("Closing camera")
                cap.release()
                return

            time_elapsed = time.time() - start_time  # Tiempo que tardó en procesar el frame
            if time_elapsed < frame_time:
                time.sleep(frame_time - time_elapsed)  # Pausa para mantener los FPS deseados
        print("Closing camera")

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@stream_bp.route('/stream.html', methods=['GET'])
def stream_html():
    return render_template_string("""
    <html>
        <head>
            <title>Stream</title>
        </head>
        <body>
            <img src="{{ url_for('stream.stream') }}" />
        </body>
    </html>
    """)