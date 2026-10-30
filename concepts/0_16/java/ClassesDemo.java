public class ClassesDemo {
    static final class Ticket {
        private final int id;
        Ticket(int id) { this.id = id; }
        int getId() { return id; }
    }
    public static void main(String[] args) {
        System.out.println(new Ticket(7).getId());
    }
}
