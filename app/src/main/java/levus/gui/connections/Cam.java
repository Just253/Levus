package levus.gui.connections;

import io.socket.client.Socket;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.HBox;
import javafx.application.Platform;
import javafx.scene.control.ToggleButton;

public class Cam {
  private final Socket_manager socket_manager;
  private Socket socket;
  private ImageView camImage;
  public Boolean isOn = false;
  private ToggleButton toggleCamButton;

  public Cam(Socket_manager socket_manager) {
    this.socket_manager = socket_manager;
    this.setSocket(socket_manager.getSocket());
    this.makeImage();
    this.add_listeners();
  }
  public void setSocket(Socket socket) {
    this.socket = socket;
  }

  public Socket getSocket() {
    return this.socket;
  }

  public void add_listeners() {
    socket.on("ToggleCam", args -> {
        isOn = (Boolean) args[0];
        toggleCam(isOn);

    });
  }

  private void receiveImage(Object... args) {
    String base64Image = (String) args[0];

    Platform.runLater(() -> {
        Image image = new Image("data:image/png;base64," + base64Image);
        camImage.setImage(image);
    });
  }

  public void toggleCam(Boolean isOn) {
    toggleCamButton.setSelected(isOn);
    Platform.runLater(() -> {
        VBox contentApp = (VBox) socket_manager.getStage().getScene().lookup("#appContent");
        if (isOn) {
            if (!contentApp.getChildren().contains(camImage)) {
                contentApp.getChildren().add(camImage);
            }
            // Activar la escucha del evento "receiveImage"
            socket.on("receiveImage", this::receiveImage);
        } else {
            contentApp.getChildren().remove(camImage);
            // Desactivar la escucha del evento "receiveImage"
            socket.off("receiveImage");
        }
    });
    socket.emit("toggleCam", isOn);
  }

  public void makeImage() {
    // TODO: LOAD FXML
    camImage = new ImageView();
    camImage.setFitWidth(640);
    camImage.setFitHeight(480);

  }

  public void setToggleCamButton(ToggleButton toggleCamButton) {
    this.toggleCamButton = toggleCamButton;
  }
}