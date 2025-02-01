package Server.Handler;

import LLM.LocalClient.Ollama;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import org.json.JSONObject;
import java.io.IOException;

/**
 * The {@code ListModelsHandler} class handles HTTP GET requests to retrieve a list
 * of available models from the local {@link Ollama} client.
 * <p>
 * This handler extends {@link ResponseSender} to simplify sending JSON responses.
 */
public class ListModelsHandler extends ResponseSender implements HttpHandler {

    /**
     * Instance of the {@link Ollama} client for interacting with local models.
     */
    private final Ollama ollama;

    /**
     * Constructs a new {@code ListModelsHandler} and initializes the {@link Ollama} client.
     */
    public ListModelsHandler() {
        this.ollama = new Ollama();
    }

    /**
     * Handles incoming HTTP GET requests to retrieve the list of models.
     * <p>
     * If the request method is not GET, a 405 Method Not Allowed response is sent.
     * Otherwise, the handler fetches the list of models from {@link Ollama}
     * and returns it as a JSON response.
     *
     * @param exchange the {@link HttpExchange} object for the HTTP request and response.
     * @throws IOException if an error occurs while processing the request or response.
     */
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        // Check if the request method is GET
        if (!exchange.getRequestMethod().equalsIgnoreCase("GET")) {
            exchange.sendResponseHeaders(405, -1); // Method Not Allowed
            return;
        }

        try {
            // Retrieve the list of models
            var models = ollama.listModels();

            // Create the JSON response
            JSONObject responseJson = new JSONObject();
            responseJson.put("models", models);

            // Send the successful response
            sendResponse(exchange, responseJson.toString(), 200);

        } catch (IOException e) {
            // Handle errors during model retrieval
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Fehler beim Abrufen der Modelle: " + e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 500);
        }
    }
}
