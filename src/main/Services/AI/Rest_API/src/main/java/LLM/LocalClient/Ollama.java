package LLM.LocalClient;

import LLM.HttpClient;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * The {@code Ollama} class provides an interface to manage and interact with local
 * language models via an API. It supports model management operations such as loading,
 * unloading, and querying available or active models.
 * <p>
 * This class depends on {@link HttpClient} for HTTP communication with the local
 * Ollama server.
 */
public class Ollama {

    private final HttpClient httpClient;
    private String serverUrl;
    private final String OllamaServerURL = "http://localhost:11434";
    private Model model;

    /**
     * Enum representing the available language models on the Ollama server.
     */
    public enum Model {
        TINY_LLAMA("tinyllama"),
        LLAMA3_1("llama3.1:8b"),
        LLAMA3_2_3B("llama3.2:3b"),
        LLAMA2_UNCENSORED("llama2-uncensored:7b"),
        MOONDREAM("moondream");

        private final String modelName;

        Model(String modelName) {
            this.modelName = modelName;
        }

        /**
         * Retrieves the model name as a string.
         *
         * @return the model name.
         */
        public String getModelName() {
            return modelName;
        }
    }

    /**
     * Constructs an {@code Ollama} instance and initializes it with a default server URL
     * and model.
     */
    public Ollama() {
        serverUrl = OllamaServerURL;
        this.httpClient = new HttpClient(serverUrl);
        setModel(Model.LLAMA3_2_3B);
    }

    /**
     * Sets the active model for the Ollama server. If the model is not already loaded,
     * it will be loaded.
     *
     * @param model the {@link Model} to be set as active.
     */
    public void setModel(Model model) {
        this.model = model;

        try {
            if (!unloadAllExcept(model)) {
                loadModel(model);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * Generates a non-streaming response from the active model based on the provided prompt.
     *
     * @param prompt the input prompt for the model.
     * @return the generated response as a string.
     * @throws IOException if an error occurs during communication with the server or response processing.
     */
    public String generateResponseNonStreaming(String prompt) throws IOException {
        JSONObject payload = new JSONObject();
        payload.put("model", model.getModelName());
        payload.put("prompt", prompt);
        payload.put("stream", false);

        String response = httpClient.postRequest("/api/generate", payload.toString());

        JSONObject jsonResponse = new JSONObject(response);

        if (!jsonResponse.has("response")) {
            throw new IOException("The API response does not contain a 'response' field: " + response);
        }

        return jsonResponse.getString("response");
    }

    /**
     * Lists all available models on the server.
     *
     * @return a list of model names as strings.
     * @throws IOException if an error occurs while fetching the model list.
     */
    public List<String> listModels() throws IOException {
        String response = httpClient.getRequest("/api/tags");

        JSONObject jsonResponse = new JSONObject(response);
        return jsonResponse.getJSONArray("models").toList().stream()
                .map(model -> new JSONObject((HashMap<?, ?>) model))
                .map(json -> json.getString("name"))
                .toList();
    }

    /**
     * Lists all currently running models on the server.
     *
     * @return a list of running {@link Model} instances.
     * @throws IOException if an error occurs while fetching the running models.
     */
    public List<Model> listRunningModels() throws IOException {
        String response = httpClient.getRequest("/api/ps");

        JSONObject jsonResponse = new JSONObject(response);
        if (!jsonResponse.has("models")) {
            throw new IOException("The API response does not contain a 'models' field: " + response);
        }

        List<Model> runningModels = new ArrayList<>();
        for (Object modelObject : jsonResponse.getJSONArray("models")) {
            JSONObject modelJson = (JSONObject) modelObject;
            String modelName = modelJson.getString("model");

            Model enumModel = getModelFromName(modelName);
            if (enumModel != null) {
                runningModels.add(enumModel);
            } else {
                System.out.println("Unknown model: " + modelName);
            }
        }

        return runningModels;
    }

    private Model getModelFromName(String modelName) {
        for (Model model : Model.values()) {
            if (model.getModelName().equalsIgnoreCase(modelName)) {
                return model;
            }
        }
        return null;
    }

    /**
     * Loads the specified model on the server.
     *
     * @param model the {@link Model} to be loaded.
     * @return {@code true} if the model was successfully loaded; otherwise, {@code false}.
     * @throws IOException if an error occurs during the loading process.
     */
    public boolean loadModel(Model model) throws IOException {
        JSONObject payload = new JSONObject();
        payload.put("model", model.getModelName());

        String response = httpClient.postRequest("/api/generate", payload.toString());

        JSONObject jsonResponse = new JSONObject(response);
        if (jsonResponse.has("done") && jsonResponse.getBoolean("done")) {
            return true;
        } else {
            throw new IOException("The model could not be loaded: " + response);
        }
    }

    /**
     * Unloads the specified model from the server.
     *
     * @param model the {@link Model} to be unloaded.
     * @return {@code true} if the model was successfully unloaded; otherwise, {@code false}.
     * @throws IOException if an error occurs during the unloading process.
     */
    public boolean unloadModel(Model model) throws IOException {
        JSONObject payload = new JSONObject();
        payload.put("model", model.getModelName());
        payload.put("keep_alive", 0);

        String response = httpClient.postRequest("/api/generate", payload.toString());

        JSONObject jsonResponse = new JSONObject(response);
        if (jsonResponse.has("done") && jsonResponse.getBoolean("done") &&
                jsonResponse.optString("done_reason", "").equalsIgnoreCase("unload")) {
            return true;
        } else {
            throw new IOException("The model could not be unloaded: " + response);
        }
    }

    /**
     * Unloads all currently running models except for the specified one.
     *
     * @param modelToKeep the {@link Model} to keep running.
     * @return {@code true} if the specified model is already running; otherwise, {@code false}.
     * @throws IOException if an error occurs during the unloading process.
     */
    public boolean unloadAllExcept(Model modelToKeep) throws IOException {
        List<Model> runningModels = listRunningModels();

        boolean isWantedModelActive = false;

        for (Model model : runningModels) {
            if (model.equals(modelToKeep)) {
                isWantedModelActive = true;
                continue;
            }

            try {
                if (unloadModel(model)) {
                    System.out.println("Model successfully unloaded: " + model.getModelName());
                }
            } catch (IOException e) {
                System.err.println("Error unloading model: " + model.getModelName() + " - " + e.getMessage());
            }
        }
        return isWantedModelActive;
    }
}
