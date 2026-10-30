public class CacheDemo {
    public static String cached(String key) {
        return "hit:" + key;
    }
    public static void main(String[] args) {
        System.out.println(cached("auth"));
        System.out.println(cached("auth"));
    }
}
