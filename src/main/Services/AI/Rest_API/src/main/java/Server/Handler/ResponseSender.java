package Server.Handler;

import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

/**
 * The {@code ResponseSender} class provides a utility method for sending HTTP responses
 * to clients. It simplifies the process of setting response headers, status codes,
 * and writing the response body.
 * <p>
 * This class is designed to be extended by HTTP handlers that require a consistent
 * mechanism for sending JSON responses.
 */
public class ResponseSender {

    /**
     * Sends an HTTP response with the specified content and status code.
     * <p>
     * The response content type is set to "application/json" and the response body
     * is encoded using UTF-8.
     *
     * @param exchange   the {@link HttpExchange} object representing the HTTP request and response.
     * @param response   the response body as a string.
     * @param statusCode the HTTP status code for the response.
     * @throws IOException if an I/O error occurs while sending the response.
     */
    public void sendResponse(HttpExchange exchange, String response, int statusCode) throws IOException {
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(statusCode, response.getBytes(StandardCharsets.UTF_8).length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }
}
