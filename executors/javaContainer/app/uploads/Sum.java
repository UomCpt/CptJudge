import java.util.Scanner;

public class Sum {
    public static void main(String[] args) {
        // Χρήση try-with-resources για να κλείνει αυτόματα ο Scanner
        try (Scanner sc = new Scanner(System.in)) {
            int a = sc.nextInt();
            int b = sc.nextInt();
            System.out.println(a + b);
        }
    }
}
