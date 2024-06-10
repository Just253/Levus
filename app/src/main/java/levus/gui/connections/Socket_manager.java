package levus.gui.connections;

import java.io.IOException;
import java.net.Socket;

public class Socket_manager {
    private Socket socket;
    private String host;
    private int port;

    public Socket_manager(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public void connect() throws IOException {
        try {
            socket = new Socket(host, port);
        } catch (IOException e) {
            System.out.println("Connection failed | Retrying...");
            this.connect();
        }
    }
}
