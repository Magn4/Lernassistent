package LLM.ExternalClient;

import java.io.FileReader;
import java.io.IOException;
import java.util.Properties;

/**
 * The {@code ApiKeyLoader} class is responsible for loading and retrieving API keys
 * from a configuration file. This class uses a {@link Properties} object to read the
 * file and extract the API key specified under the "key" property.
 *
 * <p>Potential usage includes providing API keys to other external client components
 * such as HTTP clients that require authentication for external API interactions.
 */
public class ApiKeyLoader {

    /**
     * A {@link Properties} instance used to hold the configuration data.
     */
    private Properties properties;

    /**
     * Loads properties from the specified file path into the {@link Properties} object.
     *
     * @param filePath the path to the configuration file containing the properties.
     */
    private void loadProperties(String filePath) {
        properties = new Properties();
        try (FileReader reader = new FileReader(filePath)) {
            properties.load(reader);
        } catch (IOException e) {
            System.err.println("File " + filePath + " could not be loaded");
        }
    }

    /**
     * Retrieves the API key from the specified configuration file.
     * <p>
     * This method calls {@link #loadProperties(String)} to load the properties and
     * then extracts the API key under the "key" property. If the key is missing or empty,
     * it throws a {@link RuntimeException}.
     *
     * @param filePath the path to the configuration file containing the API key.
     * @return the API key as a {@link String}.
     * @throws IOException if an I/O error occurs while loading the file.
     * @throws RuntimeException if the API key is not found or is empty.
     */
    public String getApiKey(String filePath) throws IOException {
        loadProperties(filePath);

        String apiKey = properties.getProperty("key");
        if (apiKey == null || apiKey.isEmpty()) {
            throw new RuntimeException("API-Key nicht in der Konfigurationsdatei gefunden.");
        }
        System.out.println("Groq API Key: " + apiKey.substring(0, 3) + "***" + apiKey.substring(apiKey.length() - 3));
        return apiKey;
    }
}
