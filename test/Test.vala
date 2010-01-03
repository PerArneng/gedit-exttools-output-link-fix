// this file contains errors on purpose
using GLib;



public class Test.HelloObject : GLib.Object {

    static int get_int() {
        return "error";
    }

    public static int main(string[] args) {
        c();
        int a = "xxx";
        stdout.printf("Hello, World\n");
        return get_int();
    }
    
}

