package Server.Handler;

import LlmClient.LanguageModelClient;
import LlmClient.LanguageModelClient.Model;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class ListRunningModelsHandler implements HttpHandler {

    private final LanguageModelClient languageModelClient;

    public ListRunningModelsHandler() {
        this.languageModelClient = new LanguageModelClient();
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        if (!exchange.getRequestMethod().equalsIgnoreCase("GET")) {
            exchange.sendResponseHeaders(405, -1); // Method Not Allowed
            return;
        }

        try {
            // Laufende Modelle abrufen
            List<Model> runningModels = languageModelClient.listRunningModels();

            // JSON-Antwort erstellen
            JSONArray modelsArray = new JSONArray();
            for (Model model : runningModels) {
                JSONObject modelJson = new JSONObject();
                modelJson.put("modelName", model.getModelName());
                modelsArray.put(modelJson);
            }

            JSONObject responseJson = new JSONObject();
            responseJson.put("runningModels", modelsArray);

            sendResponse(exchange, responseJson.toString(), 200);

        } catch (IOException e) {
            // Fehlerbehandlung
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Fehler beim Abrufen der laufenden Modelle: " + e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 500);
        }
    }

    private void sendResponse(HttpExchange exchange, String response, int statusCode) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, response.getBytes(StandardCharsets.UTF_8).length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }
}
