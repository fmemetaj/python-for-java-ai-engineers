public class PinDemo {
    public static boolean pinOk(String declared, String locked) {
        return declared.equals(locked);
    }

    public static void main(String[] args) {
        System.out.println(pinOk("3.41.0", "3.41.0"));
        System.out.println(pinOk("3.41.0", "3.40.0"));
    }
}
