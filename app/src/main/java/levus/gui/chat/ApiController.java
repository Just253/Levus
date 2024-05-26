package levus.gui.chat;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

import org.json.JSONObject;
import org.json.JSONArray;

public class ApiController {
  private String url = "localhost:5000";

    public JSONObject sendMessage(JSONArray messages) {
        String model = "gpt-3.5-turbo-0125";
        String url = "http://" + this.url + "/chat";
        Map<Object, Object> data = new HashMap<>();
        data.put("model", model);
        data.put("messages", messages);
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
            return null;
        }
    };

};
