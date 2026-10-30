public class ResponsesDemo {
    sealed interface Item permits MessageItem, ReasoningItem {}
    record MessageItem(String text) implements Item {}
    record ReasoningItem(int tokens) implements Item {}
    public static void main(String[] args) {
        Item item = new MessageItem("hi");
        String out = switch (item) {
            case MessageItem m -> m.text();
            case ReasoningItem r -> "";
        };
        System.out.println(out);
    }
}
