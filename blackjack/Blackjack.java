import java.util.*;

public class Blackjack {
    List<HashMap<String, String>> stapel = new ArrayList<HashMap<String, String>>();
    HashMap<String, String> karte = new HashMap<String, String>();

    public static void main(String[] args) {
        try (Scanner scanner = new Scanner(System.in)) {
            while (true) {
                String spielWeiter = scanner.nextLine();
                spielWeiter = spielWeiter.toLowerCase();
                System.out.println(spielWeiter);
                if (spielWeiter.equals("ja") || spielWeiter.equals("j")) {
                    System.out.println("Das Spiel lauf weiter.");
                } else if (spielWeiter.equals("nein") || spielWeiter.equals("n")) {
                    System.out.println("Gestoppt");
                    break;
                } else {
                    System.out.println("Kein gultiger Befehl! (ja/nein ; j/n)");
                }
            }
        }
    }
}