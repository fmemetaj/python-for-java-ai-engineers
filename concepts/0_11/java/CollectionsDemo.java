import java.util.List;
import java.util.Map;
import java.util.Set;

public class CollectionsDemo {
    public static void main(String[] args) {
        var levels = List.of("INFO", "ERROR", "INFO");
        var unique = Set.copyOf(levels);
        var counts = Map.of("INFO", 2, "ERROR", 1);
        System.out.println(unique.size() + counts.get("INFO"));
    }
}
