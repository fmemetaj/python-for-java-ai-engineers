public class ProtocolDemo {
    interface Retriever {
        String search(String query);
    }
    static class Memory implements Retriever {
        public String search(String query) { return query; }
    }
    public static void main(String[] args) {
        Retriever r = new Memory();
        System.out.println(r.search("login"));
    }
}
