public class VectorIndexDemo {
    public static int topId(double[] q, double[][] docs) {
        int best = 0;
        double bestScore = q[0] * docs[0][0] + q[1] * docs[0][1];
        for (int i = 1; i < docs.length; i++) {
            double score = q[0] * docs[i][0] + q[1] * docs[i][1];
            if (score > bestScore) { bestScore = score; best = i; }
        }
        return best;
    }
    public static void main(String[] args) {
        System.out.println(topId(new double[]{1, 0}, new double[][]{{1, 0}, {0, 1}}));
    }
}
