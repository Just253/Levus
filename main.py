from server import create_app, socketio

app = create_app()
if __name__ == "__main__":
    print(app.url_map)
    socketio.run(app)