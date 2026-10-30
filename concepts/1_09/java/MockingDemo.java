public class MockingDemo {
    interface HttpGet { String get(String url); }
    static String title(HttpGet http, String url) {
        return http.get(url);
    }
    public static void main(String[] args) {
        System.out.println(title(u -> "{\"title\":\"Auth\"}", "/pages/auth"));
    }
}
