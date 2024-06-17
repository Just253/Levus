package levus.gui.connections;

import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.ToggleButton;
import javafx.scene.control.ToolBar;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import levus.gui.helper.ResizeHelper;
import levus.gui.helper.VideoSource;

import java.io.ByteArrayInputStream;
import java.io.IOException;

public class Cam {
    private final Socket_manager socket_manager;
    private VideoSource videoSource;
    private Boolean isOn = false;
    private ToggleButton toggleCamButton;
    private ImageView imageView; // Para mostrar imágenes del flujo
    private Stage videoStage; // Referencia al Stage de la ventana de la cámara

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
            if (isOn) {
                if (videoSource != null) {
                    videoSource.disconnect();
                }

                System.out.println("Turning on the camera");
                videoSource = new VideoSource("http://127.0.0.1:5000/stream"); // URL del flujo MJPEG
                try {
                    videoSource.connect();
                    if (videoStage == null) {
                        videoStage = newStage();
                    }
                    videoStage.show(); // Mostrar la ventana

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
                } catch (Exception e) {
                    e.printStackTrace();
                }
            } else {
                System.out.println("Turning off the camera");
                if (videoSource != null) {
                    videoSource.disconnect();
                }
                if (videoStage != null) {
                    System.out.println("Closing camera window");
                    videoStage.close(); // Cerrar la ventana
                    videoStage = null; // Eliminar la referencia para permitir la creación de una nueva ventana más tarde
                }
            }
        });
    }

    public void setToggleCamButton(ToggleButton toggleCamButton) {
        this.toggleCamButton = toggleCamButton;
    }

    public Stage newStage() {
        try {
            Stage stage = new Stage();
            stage.initStyle(StageStyle.UNDECORATED); // Ventana sin barra de título

            VBox root = new VBox(); // Usar VBox como contenedor principal

            // Cargar la barra de herramientas desde el archivo XML
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/levus/gui/fxml/titleBar.fxml"));
            ToolBar toolBar = loader.load();

            // Añadir la barra de herramientas y el ImageView al VBox
            root.getChildren().add(toolBar);
            root.getChildren().add(imageView);

            // Configurar el ImageView para que respete su tamaño
            imageView.setPreserveRatio(true);
            imageView.fitWidthProperty().bind(stage.widthProperty()); // Ajustar el ancho del ImageView al ancho del stage

            Scene scene = new Scene(root, 960, 540); // Tamaño inicial de la ventana
            stage.setScene(scene);

            ResizeHelper rh = new ResizeHelper();
            rh.addResizeListener(stage); // Asumiendo que ResizeHelper ajusta el tamaño de la ventana correctamente

            return stage;
        } catch (IOException e) {
            e.printStackTrace();
            return null; // En caso de error, retorna null o maneja el error adecuadamente
        }
    }
}