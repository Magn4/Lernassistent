package LlmClient;

public class RequestLog {
    private final String method;
    private final String endpoint;
    private final String request;
    private final int responseCode;
    private final String response;
    private final long duration;

    public RequestLog(String method, String endpoint, String request,int responseCode, String response, long duration) {
        this.method = method;
        this.endpoint = endpoint;
        this.request = request;
        this.responseCode = responseCode;
        this.response = response;
        this.duration = duration;
    }

    @Override
    public String toString() {
        return String.format("Method: %s, Endpoint: %s, Request: %s,ResponseCode: %d, Duration: %dms, Response: %s",
                method, endpoint, request,responseCode, duration, response);
    }
}