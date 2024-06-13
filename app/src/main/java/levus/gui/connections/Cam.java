package levus.gui.connections;

import io.socket.client.Socket;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.VBox;
import javafx.application.Platform;
import javafx.scene.control.ToggleButton;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.util.Duration;

public class Cam {
  private final Socket_manager socket_manager;
  private Socket socket;
  private MediaView camView;
  private MediaPlayer mediaPlayer;
  public Boolean isOn = false;
  private ToggleButton toggleCamButton;

  public Cam(Socket_manager socket_manager) {
    this.socket_manager = socket_manager;
    this.setSocket(socket_manager.getSocket());
    this.makeMedia();
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

  public void toggleCam(Boolean isOn) {
    System.out.println("toggleCam called with: " + isOn);
    toggleCamButton.setSelected(isOn);
    Platform.runLater(() -> {
        VBox contentApp = (VBox) socket_manager.getStage().getScene().lookup("#appContent");
        if (isOn) {
            System.out.println("Turning on the camera");
            if (!contentApp.getChildren().contains(camView)) {
                System.out.println("Adding camView to contentApp");
                contentApp.getChildren().add(camView);
            }
            // Activar la escucha del evento "receiveImage"
            System.out.println("Playing media");
            mediaPlayer.play();
        } else {
            System.out.println("Turning off the camera");
            contentApp.getChildren().remove(camView);
            // Desactivar la escucha del evento "receiveImage"
            System.out.println("Stopping media");
            mediaPlayer.stop();
        }
    });
    System.out.println("Emitting toggleCam event with: " + isOn);
    socket.emit("toggleCam", isOn);
  }

  public void makeMedia() {
    // TODO: Arreglarlo porque no funciona 
    String url = "http://127.0.0.1:5000/stream";
    Media media = new Media(url);
    mediaPlayer = new MediaPlayer(media);
    camView = new MediaView(mediaPlayer);
    camView.setFitWidth(640);
    camView.setFitHeight(1);

    // Agrega un EventHandler al mediaPlayer
    mediaPlayer.setOnEndOfMedia(new Runnable() {
        @Override
        public void run() {
            // Cuando el video llega al final, reinicia la reproducción
            mediaPlayer.seek(Duration.ZERO);
        }
    });
  }

  public void setToggleCamButton(ToggleButton toggleCamButton) {
    this.toggleCamButton = toggleCamButton;
  }
}