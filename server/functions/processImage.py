from ..gestureRecognition.app import main

def generate():
    images = main()
    for frame in images:
        try:
            header = (b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n'
                      b'Content-Length: ' + bytes(str(len(frame)), 'utf-8') + b'\r\n\r\n')
            footer = b'\r\n\r\n'
            yield header + frame + footer
        except Exception as e:
            print(e)
            return