import Server.RestApiServer;

import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        try {
            RestApiServer server = new RestApiServer();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
