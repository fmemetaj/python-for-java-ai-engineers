import java.util.ArrayList;

public class VariablesDemo {
    public static void main(String[] args) {
        var numbers = new ArrayList<Integer>();
        numbers.add(1);
        var alias = numbers;
        alias.add(2);
        numbers = new ArrayList<Integer>();
        System.out.println(alias.size());
    }
}
