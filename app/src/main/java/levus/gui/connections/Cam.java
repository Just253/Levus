package levus.gui.connections;

import javafx.application.Platform;
import javafx.scene.control.ToggleButton;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.VBox;
import levus.gui.helper.VideoSource;
import java.io.ByteArrayInputStream;

public class Cam {
    private final Socket_manager socket_manager;
    private VideoSource videoSource;
    private Boolean isOn = false;
    private ToggleButton toggleCamButton;
    private ImageView imageView; // Para mostrar imágenes del flujo

    public Cam(Socket_manager socket_manager) {
        this.socket_manager = socket_manager;
        this.imageView = new ImageView();
        this.imageView.setFitWidth(640); // Configurar tamaño preferido
        this.imageView.setFitHeight(480);
        this.add_listeners();
    }

    public void add_listeners() {
        socket_manager.getSocket().on("ToggleCam", args -> {
            isOn = (Boolean) args[0];
            toggleCam(isOn);
        });
    }

    public void toggleCam(Boolean isOn) {
        System.out.println("toggleCam called with: " + isOn);
        Platform.runLater(() -> {
            toggleCamButton.setSelected(isOn);
            VBox contentApp = (VBox) socket_manager.getStage().getScene().lookup("#appContent");
            if (isOn) {
                if (videoSource != null) {
                    videoSource.disconnect();
                }
                if (contentApp.getChildren().contains(imageView)) {
                    contentApp.getChildren().remove(imageView);
                }

                System.out.println("Turning on the camera");
                videoSource = new VideoSource("http://127.0.0.1:5000/stream"); // URL del flujo MJPEG
                try {
                    videoSource.connect();
                    new Thread(() -> {
                      for (byte[] img : videoSource) {
                        System.out.println("New image received");
                        Platform.runLater(() -> {
                          Image image = new Image(new ByteArrayInputStream(img));
                          if (!image.isError()) {
                            imageView.setImage(image);
                          } else {
                            System.out.println("Error loading image");
                            // Manejar el error de carga de la imagen aquí
                          }
                        });
                      }
                    }).start();
                    if (!contentApp.getChildren().contains(imageView)) {
                        System.out.println("Adding imageView to contentApp");
                        contentApp.getChildren().add(imageView);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            } else {
                System.out.println("Turning off the camera");
                if (videoSource != null) {
                    videoSource.disconnect();
                }
                if (contentApp.getChildren().contains(imageView)) {
                    System.out.println("Removing imageView from contentApp");
                    contentApp.getChildren().remove(imageView);
                }
            }
        });
    }

    public void setToggleCamButton(ToggleButton toggleCamButton) {
        this.toggleCamButton = toggleCamButton;
    }
}