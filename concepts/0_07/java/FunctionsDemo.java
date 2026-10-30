public class FunctionsDemo {
    static String greet(String name, String prefix) {
        return prefix + ", " + name;
    }

    static String greet(String name) {
        return greet(name, "Hello");
    }

    public static void main(String[] args) {
        System.out.println(greet("Ada"));
        System.out.println(greet("Ada", "Hi"));
    }
}
