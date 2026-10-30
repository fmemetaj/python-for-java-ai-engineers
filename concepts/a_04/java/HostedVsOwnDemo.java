public class HostedVsOwnDemo {
    public static String choose(boolean canEval, double ownRecall) {
        if (canEval && ownRecall >= 0.6) {
            return "own";
        }
        return "hosted";
    }

    public static void main(String[] args) {
        System.out.println(choose(true, 0.8));
        System.out.println(choose(false, 0.0));
    }
}
