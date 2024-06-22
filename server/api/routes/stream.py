from flask import Response, Blueprint, render_template_string, request, url_for
from ...functions import generate
stream_bp = Blueprint('stream', __name__)

@stream_bp.route('/stream', methods=['GET'])
def stream():
    print("Stream request")
    debug_mode = request.args.get('debug', default='false').lower() == 'true'
    if debug_mode: print("[stream camera] Debug mode:", debug_mode)
    return Response(generate(debug_mode), mimetype='multipart/x-mixed-replace; boundary=frame')

@stream_bp.route('/stream.html', methods=['GET'])
def stream_html():
    query = request.query_string.decode('utf-8')
    img_src = url_for('stream.stream') + '?' + query
    return render_template_string("""
    <html>
        <head>
            <title>Stream</title>
        </head>
        <body>
            <img src="{{ img_src }}" />
        </body>
    </html>
    """, img_src=img_src)