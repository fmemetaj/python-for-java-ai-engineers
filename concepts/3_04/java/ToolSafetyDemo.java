public class ToolSafetyDemo {
    public static boolean allowed(String name) {
        return "search_docs".equals(name);
    }
    public static void main(String[] args) {
        String name = "delete_all";
        if (!allowed(name)) {
            System.out.println("blocked");
            return;
        }
        System.out.println("run");
    }
}
