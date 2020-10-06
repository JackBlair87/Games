import javax.imageio.ImageIO;
import java.util.*;
import javax.swing.*; //For Panel
import java.awt.*; //For graphics
import java.io.*;
import java.awt.image.BufferedImage;

public class NinjaPanel extends JPanel{
   private static final long serialVersionUID = -5595525441567848011L;
   private String background = "lib/images/FruitNinjaBackground.jpg";
   private BufferedImage backgroundImage; 
   private BufferedImage mImage;

   String[] fruitOptions = {"Banana", "Bomb", "Cherry", "Coconut", "Green_Apple", "Kiwi_Fruit", "Lemon", "Lime", "Mango", "Orange", "Passionfruit", "Peach", "Pear", "Plum", "Red_Apple", "Strawberry", "Tomato", "Watermelon"};
   private ArrayList<Fruit> onScreenFruit;
   private Fruit endScreenFruit;
   private Score score;

   public NinjaPanel(){
      score = new Score(0, 0);
      endScreenFruit = new Fruit("Watermelon", 760, 390+40);
      onScreenFruit = new ArrayList<Fruit>();

      try{
         backgroundImage = ImageIO.read(new File(background));
      }catch(Exception e) { }
   }

   public void gameLoop(){
      long lastLoopTime = System.nanoTime();
      final int TARGET_FPS = 60;
      final long OPTIMAL_TIME = 1000000000 / TARGET_FPS;

      while(true){ //loop forever
         long now = System.nanoTime();
         long updateLength = now - lastLoopTime;
         lastLoopTime = now;
         double delta = updateLength / ((double)OPTIMAL_TIME);

         tick(updateLength, delta);
         
         try{
            Thread.sleep((lastLoopTime-System.nanoTime() + OPTIMAL_TIME)/1000000); //Try to wait 
         }
         catch (Exception e) {
            System.out.println("Something went wrong.");
         }
      }
   }

   public void tick(long now, double delta){
      int mousePosX = MouseInfo.getPointerInfo().getLocation().x - getLocationOnScreen().x;
      int mousePosY = MouseInfo.getPointerInfo().getLocation().y - getLocationOnScreen().y;
      //System.out.println(mousePosX + ", " + mousePosY);

      if(!Score.gameOver) {
         if(now % 30 == 0){
            onScreenFruit.add(new Fruit(fruitOptions[(int) (Math.random()*fruitOptions.length)]));
         }

         for (Fruit fruit : onScreenFruit){
            fruit.update(delta, mousePosX, mousePosY);
         }

         for(int index = 0; index < onScreenFruit.size(); index++){
            if(onScreenFruit.get(index).sliced){
               onScreenFruit.remove(index);
            }
            else if(onScreenFruit.get(index).bomb && onScreenFruit.get(index).isOffScreen(getHeight()+300)){
               onScreenFruit.remove(index);
            }
            else if(!onScreenFruit.get(index).bomb && onScreenFruit.get(index).isOffScreen(getHeight()+300)){
               Score.strike(1);
               System.out.println("" + onScreenFruit.get(index).toString());
               onScreenFruit.remove(index);
            }
         }
      }
      else{
         endScreenFruit.sliced = false;
         endScreenFruit.update(delta, mousePosX, mousePosY);
         if(endScreenFruit.sliced){
            Score.gameOver = false;
            score.resetGame(0, 0);
            onScreenFruit = new ArrayList<Fruit>();
         }
      }
      repaint();
   }

   @Override
   public void paintComponent(Graphics g){ 
      draw();
      g.drawImage(mImage,0,0,getWidth(),getHeight(),null);
   }

   public void draw(){
      mImage = new BufferedImage(getWidth(), getHeight(), BufferedImage.TYPE_INT_RGB);     
      Graphics g = mImage.getGraphics();  
      
      Map<?, ?> desktopHints = 
            (Map<?, ?>) Toolkit.getDefaultToolkit().getDesktopProperty("awt.font.desktophints");

        Graphics2D g2d = (Graphics2D) g;

        if (desktopHints != null) {
            g2d.setRenderingHints(desktopHints);
        }

      if(!Score.gameOver) {
         g.drawImage(backgroundImage, 75, 0, null);

         score.render(g, getWidth(), getHeight()); 

         for(int index = 0; index < onScreenFruit.size(); index++)
            onScreenFruit.get(index).render(g);
      }
      else{
         g.setFont(Score.largeFont);
         g.drawImage(backgroundImage, 75, 0, null);

         g.drawString("FRUIT NINJA!", getWidth()/2 - 235, 150);
         g.setFont(Score.smallFont);
         g.drawString("HIGH SCORE: " + Score.highScore, getWidth()/2 - 100, 250);
         g.drawString("Slice to Play", getWidth()/2 - 80, 560);
         endScreenFruit.render(g);
      }
   }
}