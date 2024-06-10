package levus.gui;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import levus.gui.chat.ChatController;

import java.io.IOException;
import atlantafx.base.theme.*;
import javafx.geometry.Rectangle2D;
import javafx.stage.Screen;
import levus.gui.connections.Socket_manager;
import levus.gui.helper.ResizeHelper;


public class App extends Application {
    private Socket_manager socket_manager = new Socket_manager("localhost", 5000);
    @Override
    public void start(Stage stage) throws IOException {
        Application.setUserAgentStylesheet(new Dracula().getUserAgentStylesheet());
        FXMLLoader fxmlLoader = new FXMLLoader(App.class.getResource("app.fxml"));

        // Establece un tamaño mínimo para la ventana
        stage.setMinWidth(400);
        stage.setMinHeight(400);

        // Obtén las dimensiones de la pantalla
        Rectangle2D screenBounds = Screen.getPrimary().getVisualBounds();
        Scene scene = new Scene(fxmlLoader.load(), screenBounds.getWidth()/4, screenBounds.getHeight()/4);
        ChatController controller = fxmlLoader.getController();
        controller.setPrimaryStage(stage);

        stage.setUserData(controller);
        scene.setFill(Color.TRANSPARENT);
        stage.initStyle(StageStyle.TRANSPARENT);
        stage.setTitle("Levus");
        stage.setScene(scene);
        ResizeHelper.addResizeListener(stage);
        stage.show();

        new Thread(() -> {
            socket_manager.setPrimaryStage(stage);
            socket_manager.setChatController(controller);
            socket_manager.connect();
        }).start();
    
    }
    public void stop() throws IOException {
        socket_manager.disconnect();
    }
    public static void main(String[] args) {
        launch(args);
    }
}