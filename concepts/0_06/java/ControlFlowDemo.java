public class ControlFlowDemo {
    static String label(int status) {
        return switch (status) {
            case 200 -> "ok";
            case 400, 404 -> "client";
            case 500 -> "server";
            default -> "other";
        };
    }

    public static void main(String[] args) {
        int sum = 0;
        for (int i = 1; i <= 3; i++) {
            sum += i;
        }
        System.out.println(label(404) + " " + sum);
    }
}
