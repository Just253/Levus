package levus.gui.chat;
import java.io.FileNotFoundException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.net.URL;

import javafx.event.ActionEvent;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import org.json.JSONArray;
import org.json.JSONObject;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.scene.layout.HBox;
import javafx.geometry.Pos;
import javafx.scene.control.ScrollPane;


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


    String config_file = "config.json";

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
            addMessages(messages);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void addMessage(JSONObject message) {
        String role = message.getString("role");
        String text = message.getString("message");
        Label label = new Label();
        //label.setMinWidth(100);
        label.setMaxWidth(chatHistory.getWidth() * 0.9);
        label.setMaxHeight(Double.MAX_VALUE);
        label.setWrapText(true);
        //label.setStyle("-fx-background-color: #333333;");
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
        message.put("message", text);
        addMessage(message);
        inputTxt.clear();
    }


    public void initialize() {
        loadChatFromFile(config_file);
    }
}
