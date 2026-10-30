import java.util.List;

public class TypeHintsDemo {
    static int first(List<Integer> items) {
        return items.get(0);
    }
    public static void main(String[] args) {
        System.out.println(first(List.of(1, 2, 3)));
    }
}
