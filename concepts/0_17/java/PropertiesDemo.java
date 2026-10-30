public class PropertiesDemo {
    static class Budget {
        private int cents;
        int getCents() { return cents; }
        void setCents(int cents) { this.cents = cents; }
    }
    public static void main(String[] args) {
        var b = new Budget();
        b.setCents(199);
        System.out.println(b.getCents());
    }
}
