package LlmClient;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Consumer;

public class HttpClient {

    private String host;
    private final List<RequestLog> logs = new ArrayList<>();
    private final ExecutorService executor = Executors.newCachedThreadPool();
    private long totalRequests = 0;
    private long successfulRequests = 0;
    private long failedRequests = 0;

    public HttpClient(String host) {
        this.host = host;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public String postRequest(String endpoint, String jsonPayload) throws IOException {
        long startTime = System.currentTimeMillis();
        URL url = new URL(host + endpoint);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json; utf-8");
        conn.setRequestProperty("Accept", "application/json");
        conn.setDoOutput(true);

        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = jsonPayload.getBytes(StandardCharsets.UTF_8);
            os.write(input, 0, input.length);
        }

        int responseCode = conn.getResponseCode();
        StringBuilder response = new StringBuilder();
        try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
        }

        logRequest("POST", endpoint, jsonPayload,responseCode, response.toString(), System.currentTimeMillis() - startTime);
        updateStatistics(responseCode);

        conn.disconnect();
        return response.toString();
    }

    public void postRequestAsync(String endpoint, String jsonPayload, Callback callback) {
        executor.submit(() -> {
            try {
                String response = postRequest(endpoint, jsonPayload);
                callback.onSuccess(response);
            } catch (IOException e) {
                callback.onError(e);
            }
        });
    }

    public String getRequest(String endpoint) throws IOException {
        long startTime = System.currentTimeMillis();
        URL url = new URL(host + endpoint);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Accept", "application/json");

        int responseCode = conn.getResponseCode();
        StringBuilder response = new StringBuilder();

        // Lesen der Antwort
        try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
        }

        logRequest("GET", endpoint, null, responseCode, response.toString(), System.currentTimeMillis() - startTime);
        updateStatistics(responseCode);

        conn.disconnect();
        return response.toString();
    }

    public void getRequestAsync(String endpoint, Callback callback) {
        executor.submit(() -> {
            try {
                String response = getRequest(endpoint);
                callback.onSuccess(response);
            } catch (IOException e) {
                callback.onError(e);
            }
        });
    }

    public void postRequestStreaming(String endpoint, String jsonPayload, Consumer<String> onPartialResponse, Consumer<Exception> onError) {
        executor.submit(() -> {
            long startTime = System.currentTimeMillis();
            try {
                URL url = new URL(host + endpoint);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json; utf-8");
                conn.setRequestProperty("Accept", "application/json");
                conn.setDoOutput(true);

                // Senden des JSON-Payloads
                try (OutputStream os = conn.getOutputStream()) {
                    byte[] input = jsonPayload.getBytes(StandardCharsets.UTF_8);
                    os.write(input, 0, input.length);
                }

                // Lesen des Streams
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        onPartialResponse.accept(line); // Rückgabe der Teilantwort
                    }
                }

                int responseCode = conn.getResponseCode();
                logRequest("POST (Streaming)", endpoint, jsonPayload, responseCode, "Streaming response", System.currentTimeMillis() - startTime);
                updateStatistics(responseCode);

            } catch (Exception e) {
                onError.accept(e); // Fehler weitergeben
            }
        });
    }

    public List<RequestLog> getLogs() {
        return new ArrayList<>(logs);
    }

    public long getTotalRequests() {
        return totalRequests;
    }

    public long getSuccessfulRequests() {
        return successfulRequests;
    }

    public long getFailedRequests() {
        return failedRequests;
    }

    public double getSuccessRate() {
        return totalRequests == 0 ? 0 : (double) successfulRequests / totalRequests * 100;
    }

    private synchronized void logRequest(String method, String endpoint, String request, int responseCode, String response, long duration) {
        if (logs.size() == 20) {
            logs.remove(0); // FIFO: Entferne die älteste Anfrage
        }
        logs.add(new RequestLog(method, endpoint, request,responseCode, response, duration));
    }

    private synchronized void updateStatistics(int responseCode) {
        totalRequests++;
        if (responseCode >= 200 && responseCode < 300) {
            successfulRequests++;
        } else {
            failedRequests++;
        }
    }

    public interface Callback {
        void onSuccess(String response);
        void onError(Exception e);
    }
}
