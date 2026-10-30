public class ProviderDemo {
    public static String client(String profile) {
        if ("test".equals(profile) || "fake".equals(profile)) {
            return "FakeLLM";
        }
        return "LiveClient";
    }
    public static void main(String[] args) {
        System.out.println(client("fake"));
    }
}
