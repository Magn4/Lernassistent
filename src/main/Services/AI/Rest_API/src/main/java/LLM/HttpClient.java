package LLM;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Map;

/**
 * The {@code HttpClient} class provides methods to send HTTP requests
 * to a specified host. It supports GET and POST requests, including the
 * ability to add custom headers and send JSON payloads.
 * <p>
 * This class is designed for interaction with RESTful APIs and can be used
 * as a utility for other components requiring HTTP communication.
 */
public class HttpClient {

    /**
     * The base URL or host for the HTTP client.
     */
    private String host;

    /**
     * Constructs an {@code HttpClient} with the specified host.
     *
     * @param host the base URL or host for the HTTP client.
     */
    public HttpClient(String host) {
        this.host = host;
    }

    /**
     * Sends a POST request to the specified endpoint with the given JSON payload.
     *
     * @param endpoint    the endpoint relative to the host.
     * @param jsonPayload the JSON payload to include in the POST request.
     * @return the response as a string.
     * @throws IOException if an I/O error occurs during the request.
     */
    public String postRequest(String endpoint, String jsonPayload) throws IOException {
        return postRequestWithHeaders(endpoint, jsonPayload, null);
    }

    /**
     * Sends a POST request to the specified endpoint with the given JSON payload and headers.
     *
     * @param endpoint    the endpoint relative to the host.
     * @param jsonPayload the JSON payload to include in the POST request.
     * @param headers     a map of additional headers to include in the request.
     * @return the response as a string.
     * @throws IOException if an I/O error occurs during the request or if the response code is not 200.
     */
    public String postRequestWithHeaders(String endpoint, String jsonPayload, Map<String, String> headers) throws IOException {
        URL url = new URL(host + endpoint);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json; utf-8");
        conn.setRequestProperty("Accept", "application/json");
        conn.setDoOutput(true);

        // Set additional headers
        if (headers != null) {
            for (Map.Entry<String, String> entry : headers.entrySet()) {
                conn.setRequestProperty(entry.getKey(), entry.getValue());
            }
        }

        // Write the JSON payload
        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = jsonPayload.getBytes(StandardCharsets.UTF_8);
            os.write(input, 0, input.length);
        }

        int responseCode = conn.getResponseCode();
        if (responseCode != 200) {
            throw new IOException("Response code: " + responseCode);
        }

        // Read the response
        StringBuilder response = new StringBuilder();
        try (BufferedReader in = new BufferedReader(new InputStreamReader(
                conn.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
        } catch (IOException e) {
            // Handle error streams
            try (BufferedReader errorReader = new BufferedReader(new InputStreamReader(
                    conn.getErrorStream(), StandardCharsets.UTF_8))) {
                String line;
                while ((line = errorReader.readLine()) != null) {
                    response.append(line);
                }
            }
        } finally {
            conn.disconnect();
        }

        return response.toString();
    }

    /**
     * Sends a GET request to the specified endpoint.
     *
     * @param endpoint the endpoint relative to the host.
     * @return the response as a string.
     * @throws IOException if an I/O error occurs during the request.
     */
    public String getRequest(String endpoint) throws IOException {
        URL url = new URL(host + endpoint);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setRequestProperty("Accept", "application/json");

        // Read the response
        StringBuilder response = new StringBuilder();
        try (BufferedReader in = new BufferedReader(new InputStreamReader(
                conn.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
        }

        conn.disconnect();
        return response.toString();
    }
}
