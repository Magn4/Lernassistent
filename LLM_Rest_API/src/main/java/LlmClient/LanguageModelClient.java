package LlmClient;

import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.function.Consumer;

public class LanguageModelClient {

    private final HttpClient httpClient;
    private String serverUrl;
    private final String OllamaServerURL = "http://209.38.252.155:11434";
    private Model model;

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

        public String getModelName() {
            return modelName;
        }
    }

    public LanguageModelClient(String host, Model model) {
        this.httpClient = new HttpClient(host);
        setModel(model);
    }

    public LanguageModelClient(Model model) {
        serverUrl = OllamaServerURL;
        this.httpClient = new HttpClient(serverUrl);
        setModel(model);
    }

    public LanguageModelClient() {
        serverUrl = OllamaServerURL;
        this.httpClient = new HttpClient(serverUrl);
        setModel(Model.LLAMA3_2_3B);

    }

    public void setServerUrl(String url) {
        serverUrl = url;
        httpClient.setHost(serverUrl);
    }

    public void setModel(Model model) {
        this.model = model;

        try {
           if(!unloadAllExcept(model)){
               loadModel(model);
           }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }

    public String generateResponseNonStreaming(String prompt) throws IOException {
        // Erstellen des JSON-Payloads
        JSONObject payload = new JSONObject();
        payload.put("model", model.getModelName());
        payload.put("prompt", prompt);
        payload.put("stream", false);

        // Senden der Anfrage und Verarbeitung der Antwort
        String response = httpClient.postRequest("/api/generate", payload.toString());

        // Verarbeitung der JSON-Antwort
        JSONObject jsonResponse = new JSONObject(response);

        // Überprüfen, ob das Feld "response" existiert
        if (!jsonResponse.has("response")) {
            throw new IOException("Die API-Antwort enthält kein 'response'-Feld: " + response);
        }

        return jsonResponse.getString("response");
    }

    public List<String> listModels() throws IOException {
        // Anfrage senden
        String response = httpClient.getRequest("/api/tags");

        // JSON-Antwort verarbeiten
        JSONObject jsonResponse = new JSONObject(response);
        return jsonResponse.getJSONArray("models").toList().stream()
                .map(model -> new JSONObject((HashMap<?, ?>) model)) // Umwandlung in JSONObject
                .map(json -> json.getString("name")) // Name extrahieren
                .toList();
    }

    public String generateResponseWithCustomOptions(String prompt, JSONObject options, boolean stream) throws IOException {
        JSONObject payload = new JSONObject();
        payload.put("model", model.getModelName());
        payload.put("prompt", prompt);
        payload.put("options", options);
        payload.put("stream", stream);

        String response = httpClient.postRequest("/api/generate", payload.toString());
        JSONObject jsonResponse = new JSONObject(response);
        return jsonResponse.getString("response");
    }

    public void generateResponseStreaming(String prompt, Consumer<String> onPartialResponse, Consumer<Exception> onError) {
        JSONObject payload = new JSONObject();
        payload.put("model", model.getModelName());
        payload.put("prompt", prompt);

        httpClient.postRequestStreaming(
                "/api/generate",
                payload.toString(),
                partialResponse -> {
                    try {
                        JSONObject json = new JSONObject(partialResponse);
                        if (json.has("response")) {
                            onPartialResponse.accept(json.getString("response")); // Teilantwort zurückgeben
                        }
                    } catch (Exception e) {
                        onError.accept(e); // Fehler in der JSON-Verarbeitung
                    }
                },
                onError
        );
    }

    public List<Model> listRunningModels() throws IOException {
        // Senden der GET-Anfrage
        String response = httpClient.getRequest("/api/ps");

        // Verarbeitung der JSON-Antwort
        JSONObject jsonResponse = new JSONObject(response);
        if (!jsonResponse.has("models")) {
            throw new IOException("Die API-Antwort enthält kein 'models'-Feld: " + response);
        }

        // Mapping der laufenden Modelle auf das Model-Enum
        List<Model> runningModels = new ArrayList<>();
        for (Object modelObject : jsonResponse.getJSONArray("models")) {
            JSONObject modelJson = (JSONObject) modelObject;
            String modelName = modelJson.getString("model");

            // Versuchen, das Modell im Enum zu finden
            Model enumModel = getModelFromName(modelName);
            if (enumModel != null) {
                runningModels.add(enumModel);
            } else {
                System.out.println("Unbekanntes Modell: " + modelName); // Optional: Logging für unbekannte Modelle
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
        return null; // Modell nicht im Enum gefunden
    }

    public boolean loadModel(Model model) throws IOException {
        // JSON-Payload erstellen
        JSONObject payload = new JSONObject();
        payload.put("model", model.getModelName());

        // POST-Anfrage senden
        String response = httpClient.postRequest("/api/generate", payload.toString());

        // Antwort verarbeiten
        JSONObject jsonResponse = new JSONObject(response);
        if (jsonResponse.has("done") && jsonResponse.getBoolean("done")) {
            return true; // Modell erfolgreich geladen
        } else {
            throw new IOException("Das Modell konnte nicht geladen werden: " + response);
        }
    }

    public boolean unloadModel(Model model) throws IOException {
        // JSON-Payload erstellen
        JSONObject payload = new JSONObject();
        payload.put("model", model.getModelName());
        payload.put("keep_alive", 0);

        // POST-Anfrage senden
        String response = httpClient.postRequest("/api/generate", payload.toString());

        // Antwort verarbeiten
        JSONObject jsonResponse = new JSONObject(response);
        if (jsonResponse.has("done") && jsonResponse.getBoolean("done") &&
                jsonResponse.optString("done_reason", "").equalsIgnoreCase("unload")) {
            return true; // Modell erfolgreich entladen
        } else {
            throw new IOException("Das Modell konnte nicht entladen werden: " + response);
        }
    }

    public void unloadAllModels() throws IOException {
        // Alle laufenden Modelle abrufen
        List<Model> runningModels = listRunningModels();

        // Über jedes Modell iterieren und entladen
        for (Model model : runningModels) {
            try {
                if (unloadModel(model)) {
                    System.out.println("Modell erfolgreich entladen: " + model.getModelName());
                }
            } catch (IOException e) {
                System.err.println("Fehler beim Entladen des Modells: " + model.getModelName() + " - " + e.getMessage());
            }
        }
    }

    public boolean unloadAllExcept(Model modelToKeep) throws IOException {
        // Alle laufenden Modelle abrufen
        List<Model> runningModels = listRunningModels();

        boolean isWantetModelActive = false;

        // Über jedes Modell iterieren
        for (Model model : runningModels) {
            // Überspringen des Modells, das behalten werden soll
            if (model.equals(modelToKeep)) {
                System.out.println("Modell behalten: " + model.getModelName());
                isWantetModelActive = true;
                continue;
            }

            // Entladen der anderen Modelle
            try {
                if (unloadModel(model)) {
                    System.out.println("Modell erfolgreich entladen: " + model.getModelName());
                }
            } catch (IOException e) {
                System.err.println("Fehler beim Entladen des Modells: " + model.getModelName() + " - " + e.getMessage());
            }
        }
        return isWantetModelActive;
    }


}
