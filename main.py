from server import create_app, socketio

app = create_app()
if __name__ == "__main__":
    print(app.url_map)
    for namespace, events in socketio.server.handlers.items():
        print(f'Namespace: {namespace}')
        for event in events.keys():
            print(f'  Event: {event}')
    socketio.run(app)