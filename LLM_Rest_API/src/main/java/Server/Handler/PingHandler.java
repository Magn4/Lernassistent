package Server.Handler;

import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import org.json.JSONObject;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class PingHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange exchange) throws IOException {
        // Aktuelle Uhrzeit abrufen
        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String currentTime = now.format(formatter);

        // Server-Adresse abrufen
        InetSocketAddress serverAddress = exchange.getLocalAddress();
        String serverIp = serverAddress.getAddress().getHostAddress();
        int serverPort = serverAddress.getPort();

        // Client-IP-Adresse abrufen
        InetSocketAddress clientAddress = exchange.getRemoteAddress();
        String clientIp = clientAddress.getAddress().getHostAddress();

        // JSON-Objekt erstellen
        JSONObject responseJson = new JSONObject();
        responseJson.put("serverAddress", serverIp + ":" + serverPort);
        responseJson.put("clientIp", clientIp);
        responseJson.put("currentTime", currentTime);

        // JSON-Antwort als String
        String response = responseJson.toString();

        // HTTP-Antwort senden
        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.sendResponseHeaders(200, response.getBytes().length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes());
        }
    }
}
