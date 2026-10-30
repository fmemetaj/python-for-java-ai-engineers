public class ConfigDemo {
    public static void main(String[] args) {
        String profile = System.getenv().getOrDefault("APP_PROFILE", "test");
        System.out.println(profile);
    }
}
