public class FrameworkDemo {
    public static String run(String agent, String input) {
        return agent + ":" + input;
    }
    public static void main(String[] args) {
        System.out.println(run("triage", "500 after capture"));
    }
}
