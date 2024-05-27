package levus.gui.chat;

import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleButton;
import org.vosk.*;

public class VoskController {
    private TextField textField;
    private Button button;
    private ToggleButton toggleButton;
    public void Listen() {

    }
    public void  sendText() {
        this.button.fire();
    }
    public void changeText(String text) {
        textField.setText(text);
    }

    public void setTextField(TextField textField) {
        this.textField = textField;
    }

    public void setButton(Button button) {
        this.button = button;
    }

    public void disableToggleButton() {
        toggleButton.setDisable(true);
    }

    public void enableToggleButton() {
        toggleButton.setDisable(false);
    }

}
