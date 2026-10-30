public class TestingDemo {
    static void assertEquals(int expected, int actual) {
        if (expected != actual) {
            throw new IllegalStateException("not equal");
        }
    }
    public static void main(String[] args) {
        assertEquals(2, "ab".length());
    }
}
