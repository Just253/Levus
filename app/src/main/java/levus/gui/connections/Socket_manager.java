package levus.gui.connections;

import javafx.stage.Stage;

import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.emitter.Emitter;
import levus.gui.chat.ChatController;

import java.io.IOException;
import java.net.URISyntaxException;

public class Socket_manager {
    private Socket socket;
    private String host;
    private int port;
    private Stage stage;
    private ChatController chatController;
    private Cam cam;

    public Socket_manager(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public void connect() throws URISyntaxException {
        socket = IO.socket("http://" + host + ":" + port);
        setupEventListeners();
        attemptConnection(5); // Intenta conectar hasta 5 veces
        initializeComponents();
    }
    
    private void setupEventListeners() {
        socket.on(Socket.EVENT_CONNECT, args -> System.out.println("Connected!"))
              .on(Socket.EVENT_DISCONNECT, args -> System.out.println("Disconnected!"));
    }
    
    private void attemptConnection(int maxAttempts) {
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                System.out.println("Attempting to connect, try " + attempt);
                socket.connect();
                return; // Salir si la conexión es exitosa
            } catch (Exception e) {
                System.out.println("Connection failed | Retrying...");
                e.printStackTrace();
                waitForRetry();
            }
        }
        System.out.println("Failed to connect after " + maxAttempts + " attempts.");
    }
    
    private void waitForRetry() {
        try {
            Thread.sleep(2000);
        } catch (InterruptedException ie) {
            Thread.currentThread().interrupt();
        }
    }
    
    private void initializeComponents() {
        new Chat(this);
        cam = new Cam(this);
        ChatController chatController = getChatController();
        chatController.setSocket(socket);
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
    public void setChatController(ChatController chatController) {
        this.chatController = chatController;
    }
    public ChatController getChatController() {
        return this.chatController;
    }

    public Cam getCam() {
        return cam;
    }
}
