public class LlmClientDemo {
    public static void main(String[] args) {
        String profile = System.getenv().getOrDefault("LLM_PROVIDER", "fake");
        String key = System.getenv().getOrDefault("OPENAI_API_KEY", "");
        System.out.println(profile);
        System.out.println(key.length());
    }
}
