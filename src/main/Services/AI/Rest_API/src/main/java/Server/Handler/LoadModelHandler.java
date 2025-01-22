package Server.Handler;

import LLM.LocalClient.Ollama;
import LLM.LocalClient.Ollama.Model;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

/**
 * The {@code LoadModelHandler} class handles HTTP POST requests to load a specified
 * model into the {@link Ollama} client.
 * <p>
 * This handler extends {@link ResponseSender} to simplify sending JSON responses.
 */
public class LoadModelHandler extends ResponseSender implements HttpHandler {

    /**
     * Instance of the {@link Ollama} client for interacting with local models.
     */
    private final Ollama ollama;

    /**
     * Constructs a new {@code LoadModelHandler} and initializes the {@link Ollama} client.
     */
    public LoadModelHandler() {
        this.ollama = new Ollama();
    }

    /**
     * Handles incoming HTTP POST requests to load a specific model.
     * <p>
     * The request body should contain a JSON object with a "modelName" field specifying
     * the name of the model to load. If the model is valid and successfully loaded, a
     * success response is returned. Otherwise, appropriate error responses are sent.
     *
     * @param exchange the {@link HttpExchange} object for the HTTP request and response.
     * @throws IOException if an error occurs while processing the request or response.
     */
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        // Check if the request method is POST
        if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
            exchange.sendResponseHeaders(405, -1); // Method Not Allowed
            return;
        }

        // Read the request body
        InputStream requestBody = exchange.getRequestBody();
        String requestBodyString = new String(requestBody.readAllBytes(), StandardCharsets.UTF_8);

        try {
            // Parse the JSON payload
            JSONObject requestJson = new JSONObject(requestBodyString);
            if (!requestJson.has("modelName")) {
                throw new IllegalArgumentException("Das Feld 'modelName' ist erforderlich.");
            }

            String modelName = requestJson.getString("modelName");

            // Find the model in the enum
            Model modelToLoad = getModelFromName(modelName);
            if (modelToLoad == null) {
                throw new IllegalArgumentException("Ungültiger Modellname: " + modelName);
            }

            // Load the model
            boolean isLoaded = ollama.loadModel(modelToLoad);

            // Send success response
            JSONObject responseJson = new JSONObject();
            responseJson.put("modelName", modelToLoad.getModelName());
            responseJson.put("loaded", isLoaded);

            sendResponse(exchange, responseJson.toString(), 200);

        } catch (IllegalArgumentException e) {
            // Handle bad request
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 400);
        } catch (IOException e) {
            // Handle server-side errors
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Fehler beim Laden des Modells: " + e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 500);
        }
    }

    /**
     * Retrieves the {@link Model} instance corresponding to the given model name.
     *
     * @param modelName the name of the model to retrieve.
     * @return the {@link Model} instance if found, or {@code null} if not found.
     */
    private Model getModelFromName(String modelName) {
        for (Model model : Model.values()) {
            if (model.getModelName().equalsIgnoreCase(modelName)) {
                return model;
            }
        }
        return null; // Model not found in the enum
    }
}
