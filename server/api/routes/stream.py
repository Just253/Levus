from flask import Response, Blueprint, render_template_string
from ...functions import generate
stream_bp = Blueprint('stream', __name__)

@stream_bp.route('/stream', methods=['GET'])
def stream():
    print("Stream request")

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