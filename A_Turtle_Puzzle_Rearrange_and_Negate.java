import java.util.*;

public class A_Turtle_Puzzle_Rearrange_and_Negate {
    public static void main(String args[]) {
        Scanner scan = new Scanner(System.in);
        int t = scan.nextInt();
        while (t > 0) {
            int n = scan.nextInt();
            int arr[] = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = scan.nextInt();
            }
            int ans = 0;
            for (int i = 0; i < n; i++) {
                if (arr[i] < 0) {
                    ans += (arr[i] * (-1));
                } else {
                    ans += arr[i];
                }
            }
            System.out.println(ans);
            t--;
        }
    }
}