package Server;

import Server.Handler.*;

import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;

/**
 * The {@code RestApiServer} class is responsible for setting up and running a RESTful API server.
 * It uses Java's built-in HTTP server and defines multiple endpoints to handle client requests.
 * <p>
 * The server includes the following API endpoints:
 * <ul>
 *     <li><b>/api/ping:</b> Checks the server's availability.</li>
 *     <li><b>/api/generateResponse:</b> Generates a response using AI models.</li>
 *     <li><b>/api/listModels:</b> Retrieves a list of available models.</li>
 *     <li><b>/api/listRunningModels:</b> Retrieves a list of running models.</li>
 *     <li><b>/api/loadModel:</b> Loads a specified model.</li>
 * </ul>
 */
public class RestApiServer {

    /**
     * The {@link HttpServer} instance used to handle HTTP requests.
     */
    private HttpServer server;

    /**
     * Constructs a {@code RestApiServer}, initializes the server, configures API endpoints,
     * and starts the server.
     *
     * @throws IOException if an error occurs during server initialization.
     */
    public RestApiServer() throws IOException {
        server = HttpServer.create(new InetSocketAddress("0.0.0.0", 9191), 0);
        configureEndpoints();
        start();
    }

    /**
     * Configures the API endpoints by associating URLs with their respective handlers.
     */
    private void configureEndpoints() {
        createContext("/ping", new PingHandler());
        createContext("/generateResponse", new GenerateHandler());
        createContext("/listModels", new ListModelsHandler());
        createContext("/listRunningModels", new ListRunningModelsHandler());
        createContext("/loadModel", new LoadModelHandler());
    }

    /**
     * Creates a new context for a specific API endpoint.
     *
     * @param endpoint the API endpoint relative to the base path (e.g., "/ping").
     * @param handler  the {@link HttpHandler} responsible for processing requests to the endpoint.
     */
    private void createContext(String endpoint, HttpHandler handler) {
        server.createContext("/api" + endpoint, handler);
    }

    /**
     * Starts the REST API server and logs the server's address and port.
     */
    public void start() {
        server.start();
        System.out.println("Server läuft auf: http://" + server.getAddress().getHostString() + ":" + server.getAddress().getPort());
    }

    /**
     * Stops the REST API server.
     */
    public void stop() {
        server.stop(0);
        System.out.println("Server wurde gestoppt.");
    }
}
