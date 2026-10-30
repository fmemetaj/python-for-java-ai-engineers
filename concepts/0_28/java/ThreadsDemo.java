import java.util.concurrent.Executors;

public class ThreadsDemo {
    public static void main(String[] args) throws Exception {
        try (var pool = Executors.newFixedThreadPool(2)) {
            var future = pool.submit(() -> "docs");
            System.out.println(future.get());
        }
    }
}
