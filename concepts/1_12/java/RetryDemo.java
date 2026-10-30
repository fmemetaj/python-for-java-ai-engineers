public class RetryDemo {
    static boolean retry(int status) {
        return status == 429 || status >= 500;
    }
    public static void main(String[] args) {
        System.out.println(retry(503));
        System.out.println(retry(404));
    }
}
