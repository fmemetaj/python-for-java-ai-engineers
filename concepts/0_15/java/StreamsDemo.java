import java.util.List;

public class StreamsDemo {
    record Ticket(int id, String priority) {}

    static List<Integer> highIds(List<Ticket> tickets) {
        return tickets.stream()
            .filter(t -> "high".equals(t.priority()))
            .map(Ticket::id)
            .toList();
    }

    public static void main(String[] args) {
        System.out.println(highIds(List.of(new Ticket(1, "high"))));
    }
}
