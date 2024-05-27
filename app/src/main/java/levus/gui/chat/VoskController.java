package levus.gui.chat;

import javafx.application.Platform;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleButton;
import org.json.JSONObject;
import org.vosk.*;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.function.Function;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import javax.sound.sampled.*;
import javafx.concurrent.Task;

public class VoskController {
    private TextField textField;
    private Button button;
    private ToggleButton toggleButton;
    private String modelName  = "vosk-model-small-es-0.42";
    private String modelDir = "Models";
    private Model model;
    private Task<Void> listenTask;
    private Thread thread;
    private SendMessageFunction sendMessage;

    public VoskController() throws IOException, InterruptedException {
        model = getModel();
    }

    public Task<Void> listen() {
        listenTask = new Task<Void>() {
            @Override
            protected Void call() throws Exception {
                
                LibVosk.setLogLevel(LogLevel.DEBUG);

                AudioFormat format = new AudioFormat(16000f, 16, 1, true, false);
                DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
                TargetDataLine microphone;

                Recognizer recognizer = new Recognizer(model, 16000);

                microphone = getMicrophone(format);
                microphone.open(format);
                microphone.start();

                int numBytesRead;
                int CHUNK_SIZE = 4096;
                int bytesRead = 0;

                byte[] b = new byte[4096];

                while(thread != null && !thread.isInterrupted()){
                    numBytesRead = microphone.read(b, 0, CHUNK_SIZE);

                    bytesRead += numBytesRead;

                    if(recognizer.acceptWaveForm(b, numBytesRead)){
                        String resultJson = recognizer.getResult();
                        System.out.println(resultJson);
                        JSONObject result = new JSONObject(resultJson);
                        String response = result.getString("text");
                        sendText(response);
                        //changeText(response);
                    }else{
                        //System.out.println(recognizer.getPartialResult());
                        String partialResultJson = recognizer.getPartialResult();
                        JSONObject partialResult = new JSONObject(partialResultJson);
                        String response = partialResult.getString("partial");
                        changeText(response);
                        
                    }
                }

                //System.out.println(recognizer.getFinalResult());

                microphone.close();
                return null;
            }
        };
        return listenTask;
    }
    
    public void setThread(Thread thread) {
        this.thread = thread;
    }

    public Thread getThread() {
        return thread;
    }


    @SuppressWarnings("exports")
    public TargetDataLine getMicrophone(AudioFormat format) {
        DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
        TargetDataLine microphone = null;
        try {
            microphone = (TargetDataLine) AudioSystem.getLine(info);
        } catch (LineUnavailableException e) {
            e.printStackTrace();
        }
        return microphone;
    }
    public void  sendText(String text) {
        System.out.println("Sending text: " + text);
        Platform.runLater(() -> {
            this.textField.setText(text);
            this.sendMessage.apply();

        });
    }
    public void changeText(String text) {
        Platform.runLater(() -> {
            this.textField.setText(text);
        });
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
        if (this.thread != null) {
            this.thread.interrupt();
            this.thread = null;
        }
    }

    private Model getModel() throws IOException, InterruptedException {
        Path modelPath = Paths.get(modelDir, modelName).toAbsolutePath();
        System.out.println("Model path: " + modelPath);
        if (!Files.exists(modelPath)) {
            downloadAndExtractModel();
        }
        return new Model(modelPath.toString());
    }

    private void downloadAndExtractModel() throws IOException, InterruptedException {
        String modelUrl = "https://alphacephei.com/kaldi/models/" + modelName + ".zip";
        Path tempZip = Files.createTempFile("model", ".zip");
    
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(modelUrl))
                .build();
        HttpResponse<Path> response = client.send(request, HttpResponse.BodyHandlers.ofFile(tempZip));
    
        try (ZipInputStream zis = new ZipInputStream(new FileInputStream(tempZip.toFile()))) {
            ZipEntry entry = zis.getNextEntry();
            while (entry != null) {
                // Modificación aquí: elimina el nombre del modelo del nombre de la entrada
                String entryName = entry.getName().replace(modelName + "/", "");
                File file = new File(Paths.get(modelDir, modelName).toString() ,entryName);
                System.out.println("Unzipping to " + file.getAbsolutePath());
                if (entry.isDirectory()) {
                    if (!file.isDirectory() && !file.mkdirs()) {
                        throw new IOException("Failed to create directory " + file);
                    }
                } else {
                    File parent = file.getParentFile();
                    if (!parent.isDirectory() && !parent.mkdirs()) {
                        throw new IOException("Failed to create directory " + parent);
                    }
    
                    try (FileOutputStream fos = new FileOutputStream(file)) {
                        byte[] buffer = new byte[1024];
                        int length;
                        while ((length = zis.read(buffer)) > 0) {
                            fos.write(buffer, 0, length);
                        }
                    }
                }
                entry = zis.getNextEntry();
            }
        }
    
        Files.delete(tempZip);
    }

    public void setsendMessageFunction(SendMessageFunction sendMessage) {
        this.sendMessage = sendMessage;
    }

    @FunctionalInterface
    public interface SendMessageFunction {
        void apply();
    }
}
