//random 1~6 rolling
import java.util.Random;
public class what {
    public static void main(String[] args) {
        Random random = new Random();
        int num = random.nextInt(6)+1;
        System.out.println(num);
    }
}
