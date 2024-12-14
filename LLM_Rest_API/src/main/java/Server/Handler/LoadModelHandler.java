package Server.Handler;

import LlmClient.LanguageModelClient;
import LlmClient.LanguageModelClient.Model;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class LoadModelHandler implements HttpHandler {

    private final LanguageModelClient languageModelClient;

    public LoadModelHandler() {
        this.languageModelClient = new LanguageModelClient();
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
            exchange.sendResponseHeaders(405, -1); // Method Not Allowed
            return;
        }

        // Anfragekörper lesen
        InputStream requestBody = exchange.getRequestBody();
        String requestBodyString = new String(requestBody.readAllBytes(), StandardCharsets.UTF_8);

        try {
            // JSON-Payload parsen
            JSONObject requestJson = new JSONObject(requestBodyString);
            if (!requestJson.has("modelName")) {
                throw new IllegalArgumentException("Das Feld 'modelName' ist erforderlich.");
            }

            String modelName = requestJson.getString("modelName");

            // Modell im Enum finden
            Model modelToLoad = getModelFromName(modelName);
            if (modelToLoad == null) {
                throw new IllegalArgumentException("Ungültiger Modellname: " + modelName);
            }

            // Modell laden
            boolean isLoaded = languageModelClient.loadModel(modelToLoad);

            // Erfolgsantwort senden
            JSONObject responseJson = new JSONObject();
            responseJson.put("modelName", modelToLoad.getModelName());
            responseJson.put("loaded", isLoaded);

            sendResponse(exchange, responseJson.toString(), 200);

        } catch (IllegalArgumentException e) {
            // Fehlerhafte Anfrage
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 400);
        } catch (IOException e) {
            // Serverseitiger Fehler
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Fehler beim Laden des Modells: " + e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 500);
        }
    }

    private Model getModelFromName(String modelName) {
        for (Model model : Model.values()) {
            if (model.getModelName().equalsIgnoreCase(modelName)) {
                return model;
            }
        }
        return null; // Modell nicht im Enum gefunden
    }

    private void sendResponse(HttpExchange exchange, String response, int statusCode) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, response.getBytes(StandardCharsets.UTF_8).length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }
}
