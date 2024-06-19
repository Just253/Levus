package levus.gui;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import levus.gui.chat.ChatController;

import java.io.IOException;
import java.net.URISyntaxException;

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

        Thread thread = new Thread(() -> {
            controller.setSocket_manager(socket_manager);
            socket_manager.setPrimaryStage(stage);
            socket_manager.setChatController(controller);
            try {
                socket_manager.connect();
            } catch (URISyntaxException e) {
                throw new RuntimeException(e);
            }
            socket_manager.getCam().setToggleCamButton(controller.getToggleCamButton());
        });
        thread.start();
        stage.setOnCloseRequest(e -> {
            thread.interrupt();
            try {
                socket_manager.disconnect();
            } catch (IOException ex) {
//                throw new RuntimeException(ex);
            }
        });
    
    }
    public void stop() throws IOException {
        socket_manager.disconnect();
    }
    public static void main(String[] args) {
        launch(args);
    }
}