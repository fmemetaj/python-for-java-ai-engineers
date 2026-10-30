public class ToolDispatchDemo {
    interface Tool { String run(String args); }
    static final class SearchDocs implements Tool {
        public String run(String args) { return "auth page"; }
    }
    public static void main(String[] args) {
        Tool tool = new SearchDocs();
        System.out.println(tool.run("auth"));
    }
}
