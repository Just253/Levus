package levus.gui.chat;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.net.URL;
import java.util.concurrent.atomic.AtomicReference;

import io.socket.client.Socket;
import javafx.application.Platform;
import javafx.collections.ListChangeListener;
import javafx.concurrent.Task;
import javafx.event.ActionEvent;
import javafx.scene.Node;
import javafx.scene.control.*;
import javafx.scene.text.Text;
import javafx.scene.text.TextFlow;
import javafx.stage.Stage;

import levus.gui.connections.Socket_manager;
import org.json.JSONArray;
import org.json.JSONObject;
import javafx.scene.layout.VBox;
import javafx.scene.layout.HBox;
import javafx.geometry.Pos;


import javafx.fxml.FXML;

/*

[
    {
      "role:"user", 
      "message":"asdasd"
    },
    {
      "role":"assistant",
      "message":"asd"
    }
]
 */
public class ChatController {
    @FXML
    private VBox chatHistory;

    @FXML
    private ScrollPane chatBox;

    @FXML
    private TextArea inputTxt;

    @FXML
    private Button btnSendMessage;

    @FXML
    private ToggleButton micButton;

    @FXML
    private ToggleButton camButton;

    public VoskController getVoskController() {
        return voskController;
    }

    private final VoskController voskController = new VoskController();
    private JSONArray messages;
    private Stage primaryStage;
    private Socket socket;

    String config_file = "config.json";
    private Socket_manager socket_manager;

    public ChatController() throws IOException, InterruptedException {
    }

    public void loadChat(JSONObject messages) {
        addMessages(messages.getJSONArray("messages"));
    }

    public void loadChatFromFile(String filename) {
        try {
            URL resourceUrl = getClass().getResource("/levus/gui/" + filename);
            if (resourceUrl == null) {
                throw new FileNotFoundException("File " + filename + " was not found.");
            }
            Path resourcePath = Paths.get(resourceUrl.toURI());
            String content = new String(Files.readAllBytes(resourcePath), "UTF-8");
            JSONArray messages = new JSONArray(content);
            this.messages = messages;
            addMessages(messages);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public Text makeLabel(String text, String role) {
        return makeLabel(text, role, "");
    }
    public Text makeLabel(String text, String role, String ProcessId) {
        // Crea un nuevo TextFlow para el texto del mensaje
        Text textNode = new Text(text);
        textNode.setId(ProcessId);
        textNode.getStyleClass().add("messages-text");

        textNode.textProperty().addListener((observable, oldValue, newValue) -> {
            // Si el scroll estaba en la parte inferior antes de que el texto cambiara
            if (chatBox.getVvalue() == 1.0) {
                // Después de que el texto cambie, mueve el scroll a la parte inferior
                Platform.runLater(() -> chatBox.setVvalue(1.0));
            }
        });

        TextFlow textFlow = new TextFlow(textNode);
        textFlow.setMaxWidth(chatHistory.getWidth() * 0.9);
        textFlow.setPadding(new javafx.geometry.Insets(10, 10, 10, 10));
        textFlow.getStyleClass().add("messages");

        chatHistory.widthProperty().addListener((observable, oldValue, newValue) -> {
            textFlow.setMaxWidth(newValue.doubleValue() * 0.9);
        });

        HBox hBox = new HBox();
        hBox.setMinWidth(100);
        hBox.setMaxWidth(Double.MAX_VALUE);

        hBox.getChildren().add(textFlow);
        if (role.equals("user")) {
            textFlow.getStyleClass().add("messages-user");
            hBox.setAlignment(Pos.CENTER_RIGHT);
        } else {
            textFlow.getStyleClass().add("messages-assistant");
            hBox.setAlignment(Pos.CENTER_LEFT);
        }
        chatHistory.getChildren().add(hBox);

        return textNode;
    }

    public void addMessage(JSONObject message) {
        String role = message.getString("role");
        JSONArray content = message.getJSONArray("content");
        for (int i = 0; i < content.length(); i++) {
            JSONObject item = content.getJSONObject(i);
            if (item.getString("type").equals("text")) {
                String text = item.getString("text");
                makeLabel(text, role);
            }
        }
    
    }

    public void addMessages(JSONArray messages) {
        for (int i = 0; i < messages.length(); i++) {
            JSONObject message = messages.getJSONObject(i);
            addMessage(message);
        }
        chatBox.setVvalue(1.0);
    }

    @FXML
    public void sendMessageEvent(ActionEvent event) {
        Platform.runLater(() -> {
            sendMessage();
        });
    }

    public void sendMessage(){
        String text = inputTxt.getText();
        if (text.isEmpty() || text.isBlank()) {
            return;
        }
        JSONObject message = new JSONObject();
        message.put("role", "user");
        message.put("content", new JSONArray().put(new JSONObject().put("type", "text").put("text", text)));
        messages.put(message);
        inputTxt.clear();

        Platform.runLater(() -> {
            addMessage(message);
            //chatBox.setVvalue(2.0);
        });

        String model = "gpt-3.5-turbo-0125";
        JSONObject data = new JSONObject();
        data.put("model", model);
        data.put("messages", messages);
        this.socket.emit("new_message", data);
    }

    public void setPrimaryStage(Stage primaryStage) {
        this.primaryStage = primaryStage;
        initStage();
    }

    private void initStage() {
        primaryStage.setOnCloseRequest(event -> {
            voskController.stopListening();
        });
    }

    @FXML
    public void initialize() {
        loadChatFromFile(config_file);

        voskController.setTextField(inputTxt);
        voskController.setsendMessageFunction(this::sendMessage);
        voskController.setToggleButton(micButton);

        micButton.selectedProperty().addListener((observable, oldValue, newValue) -> {
            if (newValue) {
                Task<Void> listenTask = voskController.listen();
                voskController.setThread(new Thread(listenTask));
                voskController.getThread().start();
            } else {
                voskController.stopListening();
            }
        });
        camButton.selectedProperty().addListener((observable, oldValue, newValue) -> {
            socket_manager.getCam().toggleCam(newValue);
        });

        // si chat box es actualizado con un nuevo item y el scroll esta en la parte inferior, entonces el scroll se mueve a la parte inferior
        chatHistory.getChildren().addListener((ListChangeListener<Node>) c -> {
            // Si el scroll está en la parte inferior antes de añadir el nuevo mensaje
            if (chatBox.getVvalue() == 1.0) {
                // Después de añadir el nuevo mensaje, mueve el scroll a la parte inferior
                Platform.runLater(() -> chatBox.setVvalue(1.0));
            }
        });
        
    }

    public void setMessages(JSONArray messages) {
        this.messages = messages;
    }

    public JSONArray getMessages() {
        return messages;
    }

    public void setSocket(Socket socket) {
        this.socket = socket;
    }

    public Socket getSocket() {
        return socket;
    }

    public void setSocket_manager(Socket_manager socket_manager) {
        this.socket_manager = socket_manager;
    }

    public ToggleButton getToggleCamButton() {
        return camButton;
    }
}
