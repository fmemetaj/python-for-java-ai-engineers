public class HybridDemo {
    public static double fuse(double bm25, double cosine, double alpha) {
        return alpha * cosine + (1.0 - alpha) * bm25;
    }
    public static void main(String[] args) {
        System.out.println(fuse(0.8, 0.2, 0.5));
    }
}
