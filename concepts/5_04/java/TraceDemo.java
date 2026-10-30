public class TraceDemo {
    static final class Span {
        final String name;
        final long durationMs;
        Span(String name, long durationMs) {
            this.name = name;
            this.durationMs = durationMs;
        }
    }
    public static void main(String[] args) {
        System.out.println(new Span("tool.search_docs", 12).name);
    }
}
