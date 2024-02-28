import java.util.*;

public class C_Turtle_Fingers_Count_the_Values_of_k {
    public static void main(String args[]) {
        Scanner scan = new Scanner(System.in);
        int T = scan.nextInt();

        while (T-- > 0) {
            int a = scan.nextInt();
            int b = scan.nextInt();
            int l = scan.nextInt();
            int tempa = a, tempb = b;
            int x = 1, y = 1;

            while (a < l) {
                if (l % a == 0)
                    x++;
                a *= tempa;
            }

            while (b < l) {
                if (l % b == 0)
                    y++;
                b *= tempb;
            }

            Set<Integer> st = new HashSet<>();

            for (int i = 0; i <= x; i++) {
                for (int j = 0; j <= y; j++) {
                    int k = (int) (Math.pow(tempa, i) * Math.pow(tempb, j));
                    if (k <= l && l % k == 0) {
                        st.add(l / k);
                    }
                }
            }

            System.out.println(st.size());
        }
    }
}
