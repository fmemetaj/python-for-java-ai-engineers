public class ArchitectureDemo {
    public static String[] layers() {
        return new String[] {"web", "service", "repository"};
    }
    public static void main(String[] args) {
        String[] names = layers();
        System.out.println(String.join(",", names));
    }
}
