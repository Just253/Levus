package levus.gui.connections;

import javafx.stage.Stage;

import java.io.IOException;
import java.net.Socket;

public class Socket_manager {
    private Socket socket;
    private String host;
    private int port;
    private Stage stage;
    public Socket_manager(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public void connect() {
        while (true) {
            try {
                socket = new Socket(host, port);
                break; // Si la conexión es exitosa, salimos del bucle
            } catch (IOException e) {
                System.out.println("Connection failed | Retrying...");
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    }

    public void disconnect() throws IOException {
        if (socket != null) {
            socket.close();
        }
    }

    public void setPrimaryStage(Stage stage) {
        this.stage = stage;
    }
}
