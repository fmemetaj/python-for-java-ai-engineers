public class ImageCostDemo {
    public static int lowDetailTokens() {
        return 85;
    }

    public static void main(String[] args) {
        int tokens = lowDetailTokens();
        double inputPerMillion = 0.40;
        double usd = tokens * inputPerMillion / 1_000_000.0;
        System.out.println(tokens);
        System.out.println(usd);
    }
}
