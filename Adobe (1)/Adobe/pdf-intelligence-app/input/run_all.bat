package features;
import java.util.Optional;
public class withoutOptimal{
    public static  void main(String[] args){
        string name=getUserNameById(1);
        if(name!=null && name.startsWith('S')){
            System.out.println("User found:"+name);
        }
        else{
            System.out.println("User not found or  doesn't match");
        }
    }
    static string getUserById(int id){
        if(id==2)return "akash";
        return null;
    }
}