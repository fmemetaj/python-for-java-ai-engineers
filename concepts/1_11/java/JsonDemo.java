public class JsonDemo {
    record DocPage(String slug, String title, String body) {}
    public static void main(String[] args) {
        var page = new DocPage("auth", "Authentication", "Bearer token");
        System.out.println(page.slug());
    }
}
