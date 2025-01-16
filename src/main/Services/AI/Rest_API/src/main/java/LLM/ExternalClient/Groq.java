package LLM.ExternalClient;

import LLM.HttpClient;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

/**
 * The {@code Groq} class provides an interface to interact with the Groq API.
 * It facilitates sending prompts and receiving generated responses through
 * the API. The class relies on an API key for authentication and uses {@link HttpClient}
 * for HTTP communication.
 *
 * <p>This class depends on the {@link ApiKeyLoader} to retrieve the API key and
 * interacts with the Groq API to generate non-streaming chat completions.
 */
public class Groq {

    /**
     * The {@link HttpClient} instance used to communicate with the Groq API.
     */
    private final HttpClient httpClient;

    /**
     * The API key used for authenticating requests to the Groq API.
     */
    private final String apiKey;

    /**
     * Constructs a new {@code Groq} instance.
     * <p>
     * This constructor initializes the {@link HttpClient} with the base URL of the Groq API,
     * retrieves the API key using {@link ApiKeyLoader}, and prepares the instance for making
     * API requests.
     *
     * @throws IOException if an error occurs while retrieving the API key or initializing the HTTP client.
     */
    public Groq() throws IOException {
        this.httpClient = new HttpClient("https://api.groq.com");

        String jarPath = new File(ApiKeyLoader.class.getProtectionDomain().getCodeSource().getLocation().getPath())
                .getParentFile()
                .getPath();

        Path filePath = Paths.get(jarPath, "groqAPIKey.ini");

        ApiKeyLoader apiKeyLoader = new ApiKeyLoader();
        this.apiKey = apiKeyLoader.getApiKey(filePath.toString());
    }

    /**
     * Sends a prompt to the Groq API and retrieves the non-streaming response.
     * <p>
     * This method constructs the payload with a predefined model and parameters,
     * sends the HTTP POST request, and parses the response to extract the generated content.
     *
     * @param prompt the user prompt to send to the Groq API.
     * @return the generated response as a {@link String}.
     * @throws Exception if an error occurs while making the request or parsing the response.
     */
    public String generateResponseNonStreaming(String prompt) throws Exception {
        String endpoint = "/openai/v1/chat/completions";

        // Hardcoded parameters
        String model = "llama-3.3-70b-versatile";
        double temperature = 1.0;
        int maxTokens = 4500;
        double topP = 1.0;
        boolean stream = false;

        // Create the messages JSON array
        JSONArray messagesArray = new JSONArray();
        messagesArray.put(new JSONObject().put("role", "user").put("content", prompt));

        // Build the payload JSON object
        JSONObject payload = new JSONObject();
        payload.put("messages", messagesArray);
        payload.put("model", model);
        payload.put("temperature", temperature);
        payload.put("max_tokens", maxTokens);
        payload.put("top_p", topP);
        payload.put("stream", stream);

        // Prepare headers
        Map<String, String> headers = new HashMap<>();
        headers.put("Content-Type", "application/json");
        headers.put("Authorization", "Bearer " + apiKey);

        // Send the request
        String response = httpClient.postRequestWithHeaders(endpoint, payload.toString(), headers);

        JSONObject jsonObject = new JSONObject(response);

        // Extract the generated content
        JSONArray choices = jsonObject.getJSONArray("choices");
        JSONObject firstChoice = choices.getJSONObject(0);
        JSONObject message = firstChoice.getJSONObject("message");
        String content = message.getString("content");

        return content;
    }
}
