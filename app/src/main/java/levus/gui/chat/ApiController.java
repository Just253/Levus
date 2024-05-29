package levus.gui.chat;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONObject;
import org.json.JSONArray;

public class ApiController {
  private String url = "localhost:5000";

    public JSONObject sendMessage(JSONArray messages) {
        String model = "gpt-3.5-turbo-0125";
        String url = "http://" + this.url + "/chat";
        JSONArray filteredMessages = filterMessages(messages);
        Map<Object, Object> data = new HashMap<>();
        data.put("model", model);
        data.put("messages", filteredMessages);
        JSONObject json = new JSONObject(data);
        String requestBody = json.toString();
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();
        try {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            return new JSONObject(response.body());
        } catch (Exception e) {
            e.printStackTrace();
            JSONObject error = new JSONObject();    
            error.put("response", e.getMessage());
            return  error;
        }
    };
    public JSONArray filterMessages(JSONArray messages){
        return filterMessages(messages, (byte) 9);
    }
    public JSONArray filterMessages(JSONArray messages, Byte limit) {
        JSONObject systemMessage = null;
        List<JSONObject> nonSystemMessages = new ArrayList<>();
        for (int i = 0; i < messages.length(); i++) {
            JSONObject message = messages.getJSONObject(i);
            if (message.getString("role").equals("system")) {
                systemMessage = message;
            } else {
                nonSystemMessages.add(message);
            }
        }

        if (systemMessage == null) {
            throw new RuntimeException("No system message found");
        }

        int start = Math.max(0, nonSystemMessages.size() - limit);
        List<JSONObject> last9NonSystemMessages = nonSystemMessages.subList(start, nonSystemMessages.size());

        JSONArray finalMessages = new JSONArray();
        finalMessages.put(systemMessage);
        for (JSONObject message : last9NonSystemMessages) {
            finalMessages.put(message);
        }

        return finalMessages;
    }
};
