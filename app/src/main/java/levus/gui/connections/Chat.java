package levus.gui.connections;


import io.socket.client.Socket;
import javafx.application.Platform;
import javafx.scene.control.Label;
import javafx.scene.text.Text;
import javafx.scene.text.TextFlow;
import javafx.stage.Stage;
import levus.gui.chat.ChatController;
import org.json.JSONArray;
import org.json.JSONObject;

public class Chat {
    private final Socket_manager socket_manager;
    private Socket socket;
    public Chat(Socket_manager socket_manager) {
        this.socket_manager = socket_manager;
        this.setSocket(socket_manager.getSocket());
        add_listeners();

    }

    public void setSocket(Socket socket) {
        this.socket = socket;
    }

    public void add_listeners() {
        socket.on("chunks", args -> {
            // example of data {'process_id': 'd5f8ae60-81b6-458f-b704-9e63942064b9', 'content': 'Se abrió YouTube en tu navegador. ¿Hay algo más en lo que pueda ayudarte?'}
            System.out.println(args[0]);
            JSONObject data = (JSONObject) args[0];
            String process_id = data.getString("process_id");
            String content = data.getString("content");

            Stage stage = socket_manager.getStage();
            // element with id process_id
            Text message = (Text) stage.getScene().lookup("#" + process_id);

            Platform.runLater(() -> {
                if (message == null) {
                    ChatController chatController = socket_manager.getChatController();
                    chatController.makeLabel(content, "assistant", process_id);
                }
                assert message != null;
                message.setText(content);
            });
        });

        socket.on("add_messages", args -> {
            ChatController chatController = socket_manager.getChatController();
            JSONObject data = (JSONObject) args[0];
            String process_id = data.getString("process_id");
            JSONArray new_messages = data.getJSONArray("messages");
            JSONArray messages = chatController.getMessages();
            // add new messages to the existing messages
            for (int i = 0; i < new_messages.length(); i++) {
                messages.put(new_messages.getJSONObject(i));
            }
            chatController.setMessages(messages);
        });

        socket.on("response_id", args -> {
            JSONObject data = (JSONObject) args[0];
            String process_id = data.getString("process_id");
            ChatController chatController = socket_manager.getChatController();
            Platform.runLater(() -> {
                chatController.makeLabel("...", "assistant", process_id);
            });

        });
    }
}
