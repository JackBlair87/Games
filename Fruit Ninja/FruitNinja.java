import javax.swing.JFrame; //For the JFrame

public class FruitNinja{
   private static NinjaPanel ninja;
   
   public static void main(String[] args) throws InterruptedException{
      JFrame frame = new JFrame("Fruit Ninja!");
      frame.setExtendedState(JFrame.MAXIMIZED_BOTH); //Full screen
      frame.setLocationRelativeTo(null);
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      ninja = new NinjaPanel();
      frame.getContentPane().add(ninja);
      frame.setVisible(true);
      ninja.gameLoop();
   }
}