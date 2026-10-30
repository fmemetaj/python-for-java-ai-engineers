import java.util.List;

public class FirstClassDemo {
    public static void main(String[] args) {
        List<String> words = List.of("login", "api");
        var sorted = words.stream()
            .sorted((a, b) -> Integer.compare(a.length(), b.length()))
            .toList();
        System.out.println(sorted);
    }
}
