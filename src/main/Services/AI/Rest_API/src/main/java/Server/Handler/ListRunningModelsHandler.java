package Server.Handler;

import LLM.LocalClient.Ollama;
import LLM.LocalClient.Ollama.Model;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.util.List;

/**
 * The {@code ListRunningModelsHandler} class handles HTTP GET requests to retrieve a list
 * of currently running models from the {@link Ollama} client.
 * <p>
 * This handler extends {@link ResponseSender} to simplify sending JSON responses.
 */
public class ListRunningModelsHandler extends ResponseSender implements HttpHandler {

    /**
     * Instance of the {@link Ollama} client for interacting with local models.
     */
    private final Ollama ollama;

    /**
     * Constructs a new {@code ListRunningModelsHandler} and initializes the {@link Ollama} client.
     */
    public ListRunningModelsHandler() {
        this.ollama = new Ollama();
    }

    /**
     * Handles incoming HTTP GET requests to retrieve the list of running models.
     * <p>
     * If the request method is not GET, a 405 Method Not Allowed response is sent.
     * Otherwise, the handler fetches the list of running models from {@link Ollama}
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
            // Retrieve the list of running models
            List<Model> runningModels = ollama.listRunningModels();

            // Create the JSON response
            JSONArray modelsArray = new JSONArray();
            for (Model model : runningModels) {
                JSONObject modelJson = new JSONObject();
                modelJson.put("modelName", model.getModelName());
                modelsArray.put(modelJson);
            }

            JSONObject responseJson = new JSONObject();
            responseJson.put("runningModels", modelsArray);

            // Send the successful response
            sendResponse(exchange, responseJson.toString(), 200);

        } catch (IOException e) {
            // Handle errors during model retrieval
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Fehler beim Abrufen der laufenden Modelle: " + e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 500);
        }
    }
}
