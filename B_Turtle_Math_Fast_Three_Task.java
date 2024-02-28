import java.util.*;

public class B_Turtle_Math_Fast_Three_Task {
    /**
     * @param args
     */
    public static void main(String args[]) {
        Scanner scan = new Scanner(System.in);
        int t = scan.nextInt();
        while (t > 0) {
            int n = scan.nextInt();
            int arr[] = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = scan.nextInt();
            }
            int sum = 0;
            Map<Integer,Integer> mp=new HashMap<>();
            for (int i = 0; i < n; i++) {
                sum+=arr[i];
                int mod=(arr[i]%3);
                int val=mp.getOrDefault(mod,0);
                mp.put(mod,val+1);
            }
            if(sum%3==0)
            System.out.println("0");
            else if(sum%3==1)
            {
                if(mp.containsKey(1)==true)
                    System.out.println("1");
                else 
                    System.out.println("2");
            }
            else if(sum%3==2)
            {
                if(mp.containsKey(2)==true || mp.containsKey(1)==true)
                    System.out.println("1");
                else 
                    System.out.println("1");
            }
            t--;
        }
    }
}