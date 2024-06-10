package levus.gui.connections;

import javafx.stage.Stage;

import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.emitter.Emitter;
import levus.gui.chat.ChatController;

import java.io.IOException;

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
                socket = IO.socket("http://" + host + ":" + port);
                socket.on(Socket.EVENT_CONNECT, new Emitter.Listener() {
                    @Override
                    public void call(Object... args) {
                        System.out.println("Connected!");
                    }
                }).on(Socket.EVENT_DISCONNECT, new Emitter.Listener() {
                    @Override
                    public void call(Object... args) {
                        System.out.println("Disconnected!");
                    }
                });
                Chat chat = new Chat(this);
                socket.connect();
                break; // Si la conexión es exitosa, salimos del bucle
            } catch (Exception e) {
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

    public Socket getSocket() {
        return socket;
    }

    public Stage getStage() {
        return stage;
    }

    public ChatController getChatController() {
        return (ChatController) stage.getScene().getUserData();
    }
}
