public class DataclassesDemo {
    record Ticket(int id, String subject) {}
    public static void main(String[] args) {
        var t = new Ticket(1, "Login");
        System.out.println(t.id() + " " + t.subject());
    }
}
