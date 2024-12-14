package Server.Handler;

import LlmClient.LanguageModelClient;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;



public class GenerateResponseNonStreamingHandler implements HttpHandler {

    private LanguageModelClient languageModelClient = new LanguageModelClient();

    // Konstruktor, um den LanguageModelClient zu injizieren
    public GenerateResponseNonStreamingHandler() {
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        // Prüfen, ob die Methode POST ist
        if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
            exchange.sendResponseHeaders(405, -1); // Method Not Allowed
            return;
        }

        // Anfragekörper lesen
        InputStream requestBody = exchange.getRequestBody();
        String requestBodyString = new String(requestBody.readAllBytes(), StandardCharsets.UTF_8);

        // JSON parsen
        JSONObject requestJson = new JSONObject(requestBodyString);
        if (!requestJson.has("prompt")) {
            // Fehlermeldung senden, falls "prompt" fehlt
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Das Feld 'prompt' ist erforderlich.");
            sendResponse(exchange, errorResponse.toString(), 400);
            return;
        }

        String prompt = requestJson.getString("prompt");

        try {
            // Antwort vom LanguageModelClient generieren
            String generatedResponse = languageModelClient.generateResponseNonStreaming(prompt);

            // Erfolgreiche Antwort zurücksenden
            JSONObject responseJson = new JSONObject();
            responseJson.put("response", generatedResponse);
            sendResponse(exchange, responseJson.toString(), 200);
        } catch (IOException e) {
            // Fehlerbehandlung
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Fehler beim Generieren der Antwort: " + e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 500);
        }
    }

    // Methode, um die HTTP-Antwort zu senden
    private void sendResponse(HttpExchange exchange, String response, int statusCode) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, response.getBytes(StandardCharsets.UTF_8).length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }
}
