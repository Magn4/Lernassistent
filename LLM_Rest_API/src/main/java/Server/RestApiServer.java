package Server;

import Server.Handler.*;

import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;

public class RestApiServer {

    private HttpServer server;

    // Konstruktor: Server konfigurieren
    public RestApiServer() throws IOException {
        server = HttpServer.create(new InetSocketAddress("localhost", 9191), 0);
        configureEndpoints();
        start();
    }

    // Endpoints definieren

    private void configureEndpoints() {
        createContext("/ping", new PingHandler());
        createContext("/generateResponseNonStreaming", new GenerateResponseNonStreamingHandler());
        createContext("/listModels", new ListModelsHandler());
        createContext("/listRunningModels", new ListRunningModelsHandler());
        createContext("/loadModel", new LoadModelHandler());
        createContext("/setServerUrl", new SetServerUrlHandler());
        createContext("/generateResponseStreaming", new GenerateResponseStreamingHandler());
    }


    private void createContext(String endpoint, HttpHandler handler) {
        server.createContext("/api" +endpoint, handler);
    }

    // Server starten
    public void start() {
        server.start();
        System.out.println("Server läuft auf: http://" + server.getAddress().getHostString() + ":" + server.getAddress().getPort());
    }

    // Server stoppen
    public void stop() {
        server.stop(0);
        System.out.println("Server wurde gestoppt.");
    }
}

