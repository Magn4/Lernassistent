package Server.Handler;

import LlmClient.LanguageModelClient;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class SetServerUrlHandler implements HttpHandler {

    private final LanguageModelClient languageModelClient;

    public SetServerUrlHandler() {
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
            if (!requestJson.has("serverUrl")) {
                throw new IllegalArgumentException("Das Feld 'serverUrl' ist erforderlich.");
            }

            String serverUrl = requestJson.getString("serverUrl");

            // Server-URL setzen
            languageModelClient.setServerUrl(serverUrl);

            // Erfolgsantwort senden
            JSONObject responseJson = new JSONObject();
            responseJson.put("serverUrl", serverUrl);
            responseJson.put("status", "updated");

            sendResponse(exchange, responseJson.toString(), 200);

        } catch (IllegalArgumentException e) {
            // Fehlerhafte Anfrage
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 400);
        } catch (Exception e) {
            // Serverseitiger Fehler
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Fehler beim Setzen der Server-URL: " + e.getMessage());
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
