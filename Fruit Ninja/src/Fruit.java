import java.awt.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.*;

public class Fruit{
    private BufferedImage fruitImage;
    private String fruit = ""; 
    public boolean sliced = false;
    public boolean bomb = false;
    private boolean fixed = false;

    private int xPos;
    private int yPos;
    private double xVelocity;
    private double yVelocity;
    
    public Fruit(String fruitWord){
        fruit = fruitWord;
        sliced = false;
        bomb = (fruitWord == "Bomb");
        fixed = false;

        xPos = 200 + (int) (Math.random() * 1040);
        yPos = 900;
        if(xPos > 1440/2) //if its on the right side of the screen
            xVelocity = -1 * (int) (Math.random() * 3) - 1;
        else
            xVelocity = (1 * (int) (Math.random() * 3)) + 1;

        yVelocity = -10;

        try{
            fruitImage = ImageIO.read(new File("lib/images/" + fruit + ".png"));
        }catch(Exception e) { 
            System.out.println("Error!");
        }
    }

    public Fruit(String fruitWord, int startX, int startY){
        fruit = fruitWord;
        sliced = false;
        bomb = (fruit == "Bomb");
        fixed = true;

        xPos = startX;
        yPos = startY;
        yVelocity = -10;
        if(xPos > 1440/2) //if its on the right side of the screen
            xVelocity = -1 * (int) (Math.random() * 3) - 1;
        else
            xVelocity = (1 * (int) (Math.random() * 3)) + 1;

        try{
            fruitImage = ImageIO.read(new File("lib/images/" + fruit + ".png"));
        }catch(Exception e) { }
    }

    public void update(double delta, int xMouse, int yMouse){
        if(!fixed){
            yVelocity += 0.07;
            xPos += (int) (xVelocity * delta);
            yPos += (int) (yVelocity * delta);
        }

        sliceFruit(xMouse, yMouse, 80);
    }

    public void sliceFruit(int mousePositionX, int mousePositionY, int benchmark){
        double orangeLine = Math.sqrt(Math.pow(xPos - mousePositionX, 2) + Math.pow(yPos - mousePositionY, 2));
        //System.out.println(orangeLine);
        
        if(orangeLine <= benchmark && sliced == false){
            sliced = true;
            if(bomb==true){
                Score.strike(3);
                System.out.println("Game ended because bomb was sliced");
            }
            else
                Score.addPoints(1);
        }
    }

    public void render(Graphics g){
        System.out.println("Drawing");
        g.drawImage(fruitImage, xPos-130, yPos-130, null);
    }

    public boolean isOffScreen(int screenLimit){
        return yPos >= screenLimit && yVelocity > 0;
    }

    public String toString(){
        return fruit + " fruit at (" + xPos + ", " + yPos + "). Bomb is " + bomb + ". Sliced is " + sliced;
    }
}