package levus.gui.chat;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.net.URL;

import javafx.application.Platform;
import javafx.concurrent.Task;
import javafx.event.ActionEvent;
import javafx.scene.control.*;
import org.json.JSONArray;
import org.json.JSONObject;
import javafx.scene.layout.VBox;
import levus.gui.chat.ApiController;
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
    private TextField inputTxt;

    @FXML
    private Button btnSendMessage;

    @FXML
    private ToggleButton micButton;

    private VoskController voskController = new VoskController();
    private JSONArray messages;
    String config_file = "config.json";

    public ChatController() throws IOException {
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

    public void addMessage(JSONObject message) {
        String role = message.getString("role");
        JSONArray content = message.getJSONArray("content");
        for (int i = 0; i < content.length(); i++) {
            JSONObject item = content.getJSONObject(i);
            if (item.getString("type").equals("text")) {
                String text = item.getString("text");
                Label label = new Label();
                label.setMaxWidth(chatHistory.getWidth() * 0.9);
                label.setMaxHeight(Double.MAX_VALUE);
                label.setWrapText(true);
                label.setPadding(new javafx.geometry.Insets(10, 10, 10, 10));
                label.setText(text);

                chatHistory.widthProperty().addListener((observable, oldValue, newValue) -> {
                    label.setMaxWidth(newValue.doubleValue() * 0.9);
                });

                HBox hBox = new HBox();
                hBox.setMinWidth(100);
                hBox.setMaxWidth(Double.MAX_VALUE);

                hBox.getChildren().add(label);
                if (role.equals("user")) {
                    label.getStyleClass().add("messages-user");
                    hBox.setAlignment(Pos.CENTER_RIGHT);
                } else {
                    label.getStyleClass().add("messages-assistant");
                    hBox.setAlignment(Pos.CENTER_LEFT);
                }

                chatHistory.getChildren().add(hBox);
            }
        }
        Platform.runLater(() -> {
            chatBox.setVvalue(1.0);
        });
    }

    public void addMessages(JSONArray messages) {
        for (int i = 0; i < messages.length(); i++) {
            JSONObject message = messages.getJSONObject(i);
            addMessage(message);
        }
        chatBox.setVvalue(1.0);
    }

    @FXML
    public void sendMessage(ActionEvent event) {
        String text = inputTxt.getText();
        if (text.isEmpty()) {
            return;
        }
        JSONObject message = new JSONObject();
        message.put("role", "user");
        message.put("content", new JSONArray().put(new JSONObject().put("type", "text").put("text", text)));
        messages.put(message);
        inputTxt.clear();
        addMessage(message);
        chatBox.setVvalue(1.0);
        askAssistant();
    }

    public void askAssistant() {
        Task<JSONObject> task = new Task<>() {
            @Override
            protected JSONObject call() throws Exception {
                ApiController api = new ApiController();
                return api.sendMessage(messages);
            }
        };
    
        task.setOnSucceeded(event -> {
            JSONObject messageResponse = task.getValue();
            JSONObject response = new JSONObject();
            response.put("role", "assistant");
            response.put("content", new JSONArray().put(new JSONObject().put("type", "text").put("text", messageResponse.getString("response"))));
            messages.put(response);
            addMessage(response);
            chatBox.setVvalue(1.0);
        });
    
        new Thread(task).start();
    }



    public void initialize() {
        loadChatFromFile(config_file);

        micButton.selectedProperty().addListener((observable, oldValue, newValue) -> {
            if (newValue) {
                Task<Void> listenTask = voskController.listen();
                new Thread(listenTask).start();
            } else {
                voskController.stopListening();
            }
        });
    }
}
