public class InheritanceDemo {
    static class Tool {
        String tag() { return "tool"; }
    }
    static class Search extends Tool {
        @Override String tag() { return "search"; }
    }
    public static void main(String[] args) {
        System.out.println(new Search().tag());
    }
}
