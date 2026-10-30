public class ExceptionsDemo {
    static int parse(String raw) {
        try {
            return Integer.parseInt(raw);
        } catch (NumberFormatException ex) {
            throw new IllegalArgumentException("bad status", ex);
        }
    }
    public static void main(String[] args) {
        System.out.println(parse("200"));
    }
}
