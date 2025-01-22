package Server.Handler;

import LLM.LocalClient.Ollama;
import LLM.ExternalClient.Groq;

import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

/**
 * The {@code GenerateHandler} class is an HTTP handler that processes POST requests
 * to generate a response using either the {@link Ollama} or {@link Groq} client.
 * It reads the input prompt from the request body, generates a response,
 * and sends it back as JSON.
 * <p>
 * This handler extends {@link ResponseSender} to simplify sending JSON responses.
 */
public class GenerateHandler extends ResponseSender implements HttpHandler {

    /**
     * Instance of the {@link Ollama} client for local model interaction.
     */
    private Ollama ollama = new Ollama();

    /**
     * Instance of the {@link Groq} client for external API interaction.
     * If initialization fails, this will remain {@code null}.
     */
    private Groq groq;

    // Initialize the Groq client
    {
        try {
            groq = new Groq();
        } catch (IOException e) {
            System.err.println("Groq service could not be initialized");
            groq = null;
        }
    }

    /**
     * Default constructor for {@code GenerateHandler}.
     */
    public GenerateHandler() {
    }

    /**
     * Handles incoming HTTP requests by validating the request method,
     * extracting the prompt from the request body, and generating a response
     * using the appropriate client.
     *
     * @param exchange the {@link HttpExchange} object for the HTTP request and response.
     * @throws IOException if an I/O error occurs during processing.
     */
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        // Verify the request method is POST
        if (!exchange.getRequestMethod().equalsIgnoreCase("POST")) {
            exchange.sendResponseHeaders(405, -1); // Method Not Allowed
            return;
        }

        // Read the request body
        InputStream requestBody = exchange.getRequestBody();
        String requestBodyString = new String(requestBody.readAllBytes(), StandardCharsets.UTF_8);

        // Parse the JSON input
        JSONObject requestJson = new JSONObject(requestBodyString);
        if (!requestJson.has("prompt")) {
            // Send an error response if "prompt" is missing
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Das Feld 'prompt' ist erforderlich.");
            sendResponse(exchange, errorResponse.toString(), 400);
            return;
        }

        String prompt = requestJson.getString("prompt");

        try {
            String generatedResponse = "Error";
            if (groq == null) {
                // Use Ollama if Groq is unavailable
                generatedResponse = ollama.generateResponseNonStreaming(prompt);
            } else {
                try {
                    // Use Groq to generate the response
                    generatedResponse = groq.generateResponseNonStreaming(prompt);
                } catch (IOException e) {
                    System.out.println(e.getMessage());
                    // Use Ollama if Groq request fails
                    ollama.generateResponseNonStreaming(prompt);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }

            // Send the successful response
            JSONObject responseJson = new JSONObject();
            responseJson.put("response", generatedResponse);
            sendResponse(exchange, responseJson.toString(), 200);
        } catch (IOException e) {
            // Handle errors during response generation
            JSONObject errorResponse = new JSONObject();
            errorResponse.put("error", "Fehler beim Generieren der Antwort: " + e.getMessage());
            sendResponse(exchange, errorResponse.toString(), 500);
        }
    }
}
