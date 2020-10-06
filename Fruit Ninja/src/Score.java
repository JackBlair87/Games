import java.util.*;
import java.awt.*;

public class Score{
    public static boolean gameOver = true;
    public static int highScore;
    public static int totalScore;
    public static int numStrikes;

    public static Font largeFont = new Font("Luminari", Font.BOLD, 70);
    public static Font smallFont = new Font("Luminari", Font.PLAIN, 30);

    public Score(int total, int strikes) {
        totalScore = total;
        highScore = totalScore;
        numStrikes = strikes;
    }

    public static void addPoints(int newPoints) {
        totalScore += newPoints;

        if (totalScore > highScore)
            highScore = totalScore;
    }

    public static void strike(int increase) {
        numStrikes += increase;
        if (numStrikes >= 3) {
            gameOver = true;
        }
    }

    public void resetGame(int total, int strikes) {
        totalScore = total;
        numStrikes = strikes;
        gameOver = false;
    }

    public static void endGame() {
        gameOver = true;
    }

    public void render(Graphics g, int maxWidth, int maxHeight){
        Map<?, ?> desktopHints = 
            (Map<?, ?>) Toolkit.getDefaultToolkit().getDesktopProperty("awt.font.desktophints");

        Graphics2D g2d = (Graphics2D) g;

        if (desktopHints != null) {
            g2d.setRenderingHints(desktopHints);
        }

        g.setFont(largeFont);
        g.setColor(Color.WHITE);
        g.drawString("Score: " + totalScore, 25, 80);
        g.setFont(smallFont);
        g.drawString("High Score: " + highScore, 25, 120);
        //draw Xs
        g.setFont(largeFont);
        if(numStrikes == 0){
            g.drawString("X", maxWidth-80, 80);
            g.drawString("X", maxWidth-130, 80);
            g.drawString("X", maxWidth-180, 80);
        }
        else if(numStrikes == 1){
            g.setColor(Color.RED);
            g.drawString("X", maxWidth-80, 80);
            g.setColor(Color.WHITE);
            g.drawString("X", maxWidth-130, 80);
            g.drawString("X", maxWidth-180, 80);
        }
        else if(numStrikes == 2){
            g.setColor(Color.RED);
            g.drawString("X", maxWidth-80, 80);
            g.drawString("X", maxWidth-130, 80);
            g.setColor(Color.WHITE);
            g.drawString("X", maxWidth-180, 80);
        }
        else if(numStrikes == 3){
            g.setColor(Color.RED);
            g.drawString("X", maxWidth-80, 80);
            g.drawString("X", maxWidth-130, 80);
            g.drawString("X", maxWidth-180, 80);
        }
    }
}