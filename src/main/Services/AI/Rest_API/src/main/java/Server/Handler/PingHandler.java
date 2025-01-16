package Server.Handler;

import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import org.json.JSONObject;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * The {@code PingHandler} class implements an HTTP handler that responds to client requests
 * with server status information, including the current server time, server address, and
 * client IP address.
 * <p>
 * This handler is typically used to check the server's availability and basic information.
 */
public class PingHandler implements HttpHandler {

    /**
     * Handles incoming HTTP requests by generating a JSON response containing
     * server and client information.
     *
     * @param exchange the {@link HttpExchange} object representing the HTTP request and response.
     * @throws IOException if an I/O error occurs during processing.
     */
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        // Get the current server time
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String currentTime = now.format(formatter);

        // Retrieve server address and port
        InetSocketAddress serverAddress = exchange.getLocalAddress();
        String serverIp = serverAddress.getAddress().getHostAddress();
        int serverPort = serverAddress.getPort();

        // Retrieve client IP address
        InetSocketAddress clientAddress = exchange.getRemoteAddress();
        String clientIp = clientAddress.getAddress().getHostAddress();

        // Create JSON response
        JSONObject responseJson = new JSONObject();
        responseJson.put("serverAddress", serverIp + ":" + serverPort);
        responseJson.put("clientIp", clientIp);
        responseJson.put("currentTime", currentTime);

        // Convert JSON to string
        String response = responseJson.toString();

        // Send HTTP response
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(200, response.getBytes().length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes());
        }
    }
}
