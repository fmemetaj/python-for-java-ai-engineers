public class BuiltInTypesDemo {
    public static void main(String[] args) {
        int count = 1_000_000;
        String title = "DocsDesk";
        String missing = null;
        System.out.println(title == "DocsDesk");
        System.out.println(missing == null);
        System.out.println(count + 1);
    }
}
