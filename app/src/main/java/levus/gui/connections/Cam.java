package levus.gui.connections;

import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.ToggleButton;
import javafx.scene.control.ToolBar;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
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
    private ImageView imageView;
    private Stage videoStage;
    private Thread videoThread;
    private volatile boolean running = false;

    public Cam(Socket_manager socket_manager) {
        this.socket_manager = socket_manager;
        this.imageView = new ImageView();
        this.imageView.setFitWidth(640);
        this.imageView.setFitHeight(480);
        this.videoSource = new VideoSource("http://127.0.0.1:5000/stream");
        this.add_listeners();
        setupVideoThread();
    }

    private void setupVideoThread() {
        videoThread = new Thread(() -> {
            while (true) {
                if (running) {
                    byte[] img = null;
                    try {
                        img = videoSource.getNextFrame();
                    } catch (IOException e) {
                        continue;
                    }
                    if (img != null) {
                        byte[] finalImg = img;
                        Platform.runLater(() -> {
                            //System.out.println("Updating image");
                            Image image = new Image(new ByteArrayInputStream(finalImg));
                            if (!image.isError()) {
                                imageView.setImage(image);
                            }else{
                                System.out.println("Error loading image");
                            }
                        });
                    }
                } else {
                    try {
                        Thread.sleep(100); // Reduce CPU usage when not running
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            }
        });
        videoThread.setDaemon(true);
        videoThread.start();
    }

    public void add_listeners() {
        socket_manager.getSocket().on("ToggleCam", args -> {
            Boolean tempisOn = (Boolean) args[0];
            if (tempisOn != isOn) {
                if(tempisOn) socket_manager.getChatController().getVoskController().stopListening();
                isOn = tempisOn;
                toggleCam(isOn);
            }
        });
    }

    public void toggleCam(Boolean isOn) {
        System.out.println("toggleCam called with: " + isOn);
        Platform.runLater(() -> {
            toggleCamButton.setSelected(isOn);
            if (isOn) {
                System.out.println("Turning on the camera");
                try {
                    videoSource.connect();
                    running = true;
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
                if (videoStage == null) {
                    videoStage = newStage();
                }
                videoStage.show();
            } else {
                System.out.println("Turning off the camera");
                running = false;
                videoSource.disconnect();
                if (videoStage != null) {
                    videoStage.close();
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
            stage.initStyle(StageStyle.UNDECORATED);

            VBox root = new VBox();
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/levus/gui/fxml/titleBar.fxml"));
            ToolBar toolBar = loader.load();
            root.getChildren().addAll(toolBar, imageView);

            imageView.setPreserveRatio(true);
            imageView.fitWidthProperty().bind(stage.widthProperty());
            imageView.fitHeightProperty().bind(stage.heightProperty());

            Scene scene = new Scene(root, 960, 540);
            stage.setScene(scene);

            ResizeHelper.addResizeListener(stage);

            return stage;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}