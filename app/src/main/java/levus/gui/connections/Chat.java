package levus.gui.connections;

import io.socket.client.Socket;
import javafx.application.Platform;
import javafx.scene.control.Label;
import javafx.stage.Stage;
import levus.gui.chat.ChatController;
import org.json.JSONArray;
import org.json.JSONObject;

public class Chat {
    private Socket_manager socket_manager;
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
            Label label = (Label) stage.getScene().lookup("#" + process_id);
            Platform.runLater(() -> {
                label.setText(content);
            });
        });

        socket.on("add_messages", args -> {
            ChatController chatController = socket_manager.getChatController();
            JSONObject data = (JSONObject) args[0];
            String process_id = data.getString("process_id");
            JSONArray new_messages = data.getJSONArray("messages");
            JSONArray messages = chatController.getMessages();
            // Buscar la posicion del process_id en el array de mensajes y agregrar los mensajes
            for (int i = 0; i < messages.length(); i++) {
                JSONObject message = messages.getJSONObject(i);
                if (message.getString("process_id").equals(process_id)) {
                    for (int j = 0; j < new_messages.length(); j++) {
                        messages.getJSONObject(i).getJSONArray("messages").put(new_messages.getJSONObject(j));
                    }
                    break;
                }
            }
            chatController.setMessages(messages);
        });
    }
}
