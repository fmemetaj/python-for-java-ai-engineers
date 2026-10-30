public class StructuredDemo {
    record Incident(String service, String severity, String summary) {}
    public static void main(String[] args) {
        Incident dto = new Incident("auth", "high", "token leak");
        if (dto.service().isBlank()) {
            throw new IllegalArgumentException("service");
        }
        System.out.println(dto.severity());
    }
}
