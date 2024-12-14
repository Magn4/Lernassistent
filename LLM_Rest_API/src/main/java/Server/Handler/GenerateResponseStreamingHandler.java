package Server.Handler;

import LlmClient.LanguageModelClient;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import org.json.JSONObject;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

public class GenerateResponseStreamingHandler implements HttpHandler {

    private final LanguageModelClient languageModelClient;

    public GenerateResponseStreamingHandler() {
        this.languageModelClient = new LanguageModelClient();
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
        if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
            exchange.sendResponseHeaders(405, -1); // Method Not Allowed
            return;
        }

        // Anfragekörper lesen
        String requestBody = new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8);
        JSONObject requestJson = new JSONObject(requestBody);

        if (!requestJson.has("prompt")) {
            sendResponse(exchange, "{\"error\":\"Das Feld 'prompt' ist erforderlich.\"}", 400);
            return;
        }

        String prompt = requestJson.getString("prompt");

        // Antwortstream öffnen
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(200, 0); // Chunked Transfer-Encoding

        try (OutputStream responseBody = exchange.getResponseBody()) {
            languageModelClient.generateResponseStreaming(
                    prompt,
                    partialResponse -> {
                        try {
                            // Jede Teilantwort schreiben
                            JSONObject jsonResponse = new JSONObject();
                            jsonResponse.put("response", partialResponse);
                            responseBody.write((jsonResponse.toString() + "\n").getBytes(StandardCharsets.UTF_8));
                            responseBody.flush(); // Daten sofort senden
                        } catch (IOException e) {
                            e.printStackTrace(); // Fehler im Stream-Handling
                        }
                    },
                    error -> {
                        try {
                            // Fehler senden und Stream schließen
                            JSONObject errorResponse = new JSONObject();
                            errorResponse.put("error", error.getMessage());
                            responseBody.write(errorResponse.toString().getBytes(StandardCharsets.UTF_8));
                            responseBody.flush();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
            );
        } catch (Exception e) {
            // Allgemeiner Fehler
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Fehler beim Streaming: " + e.getMessage());
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
