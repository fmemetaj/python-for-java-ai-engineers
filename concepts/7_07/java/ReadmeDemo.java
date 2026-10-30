public class ReadmeDemo {
    public static String[] sections() {
        return new String[] {"overview", "build", "run"};
    }
    public static void main(String[] args) {
        System.out.println(String.join(",", sections()));
    }
}
