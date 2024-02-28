import java.util.Scanner;
import java.util.HashSet;
import java.util.Set;

public class D_Turtle_Tenacity_Continual_Mods {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int t = scan.nextInt();
        while (t > 0) {
            int n = scan.nextInt();
            int[] arr = new int[n];
            int min = Integer.MAX_VALUE;
            boolean flag = true;
            for (int i = 0; i < n; i++) {
                arr[i] = scan.nextInt();
            }
            int count=0;
           for(int i =0;i<n;i++)
           {

                if(arr[i]<=min)
                {
                    min=arr[i];
                    if(arr[i]==min)
                    {
                        count++;
                    }
                }
           }
           if(count==1)
           {
            System.out.println("YES");
            t--;
            continue;
           }
            for (int i = 0; i < n; i++){
                if (arr[i] != min && arr[i] % min != 0) {
                    flag = false;
                    break;
                }
                // min = Math.min(arr[i], min);
            }
            if (flag==true) {
                System.out.println("NO");
            } else {
                System.out.println("YES");
            }
            t--;
        }
    }
}
