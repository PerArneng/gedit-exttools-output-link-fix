// this file contains errors on purpose
using System;

public class Test
{
   public static void Main(string[] args)
   {
      Console.WriteLine("Hello, World!");
      Console.WriteLine("You entered the following {0} command line arguments:",
         args.Length );
      int i = "xx";
      fakeMethod("mono");
   }
}
