package levus.gui.chat;

import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleButton;
import org.vosk.*;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import javax.sound.sampled.*;
import javafx.concurrent.Task;

public class VoskController {
    private TextField textField;
    private Button button;
    private ToggleButton toggleButton;
    private String modelName  = "vosk-model-small-es-0.42";
    private Model model = new Model(modelName);
    private Task<Void> listenTask;

    public VoskController() throws IOException {
    }

    public Task<Void> listen() {
        listenTask = new Task<Void>() {
            @Override
            protected Void call() throws Exception {
                
                LibVosk.setLogLevel(LogLevel.DEBUG);

                AudioFormat format = new AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 16000, 16, 2, 4,  44100, false);
                DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
                TargetDataLine microphone = null;
                SourceDataLine speakers = null;

                try {
                    Recognizer recognizer = new Recognizer(model, 12000000);
                    microphone = getMicrophone(format);
                    if(microphone == null) { return null; }
                    microphone.start();

                    ByteArrayOutputStream out = new ByteArrayOutputStream();
                    int numBytesRead;
                    int CHUNK_SIZE = 1024;
                    int bytesRead = 0;

                    DataLine.Info dataLineInfo = new DataLine.Info(SourceDataLine.class, format);
                    speakers = (SourceDataLine) AudioSystem.getLine(dataLineInfo);
                    speakers.open(format);
                    speakers.start();

                    byte[] b = new byte[4096];
                    while (bytesRead <= 100000000) {
                        numBytesRead = microphone.read(b, 0, CHUNK_SIZE);
                        bytesRead += numBytesRead;
                        out.write(b, 0, numBytesRead);

                        speakers.write(b, 0, numBytesRead);

                        if(recognizer.acceptWaveForm(b, numBytesRead)) {
                            String result = recognizer.getResult();
                            changeText(result);
                            sendText();
                        }else{
                            String partialResult = recognizer.getPartialResult();
                            changeText(partialResult);
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }finally {
                    speakers.drain();
                    speakers.close();
                    microphone.close();
                }
                return null;
            }
        };
        return listenTask;
    }
    @SuppressWarnings("exports")
    public TargetDataLine getMicrophone(AudioFormat format) {
        DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
        TargetDataLine microphone = null;
        try {
            microphone = (TargetDataLine) AudioSystem.getLine(info);
            microphone.open(format);
            microphone.start();
        } catch (LineUnavailableException e) {
            e.printStackTrace();
        }
        return microphone;
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

    public void setToggleButton(ToggleButton toggleButton) {
        this.toggleButton = toggleButton;
    }
    
    public void stopListening() {
        if (listenTask != null) {
            listenTask.cancel();
        }
    }
}
