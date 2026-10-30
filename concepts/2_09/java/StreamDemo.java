public class StreamDemo {
    public static void main(String[] args) {
        String[] events = {"response.output_text.delta", "response.completed"};
        for (String event : events) {
            System.out.println(event);
        }
    }
}
