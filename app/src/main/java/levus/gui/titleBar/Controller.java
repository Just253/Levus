package levus.gui.titleBar;

import atlantafx.base.theme.Styles;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.ToolBar;
import javafx.scene.layout.HBox;
import javafx.stage.Stage;

public class Controller {

    @FXML
    private Button closeBtn;

    @FXML
    private Button minimizeBtn;

    @FXML
    private Button maximizeBtn;

    @FXML
    private ToolBar titleBar;

    @FXML
    public void initialize() {
        // Cerrar la ventana cuando se haga clic en el botón de cierre
        closeBtn.setOnAction(event -> ((Stage) closeBtn.getScene().getWindow()).close());

        // Minimizar la ventana cuando se haga clic en el botón de minimizar
        minimizeBtn.setOnAction(event -> ((Stage) minimizeBtn.getScene().getWindow()).setIconified(true));

        // Maximizar/Restaurar la ventana cuando se haga clic en el botón de maximizar
        maximizeBtn.setOnAction(event -> {
            Stage stage = (Stage) maximizeBtn.getScene().getWindow();
            stage.setMaximized(!stage.isMaximized());
        });
    }
}