package levus.gui.connections;

import io.socket.client.Socket;

public class Chat {
    private Socket_manager socket_manager;
    private Socket Socket;
    public Chat(Socket_manager socket_manager) {
        this.socket_manager = socket_manager;
        this.setSocket(socket_manager.getSocket());
        add_listeners();

    }

    public void setSocket(Socket socket) {
        this.Socket = socket;
    }

    public void add_listeners() {
        // Add listeners here
    }
}
