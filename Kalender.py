"""
Kalender App.
Eine Kalender Anwendung zur Verwaltung von Terminen.
Funktionen:
Termin Objekte mit Datum, Zeit und Titel
Json Speicherung und Laden
Terminanzeige, Hinzufügen, Löschen und Monatskalender
Yasemin Senel
11.12.2025
"""
from datetime import datetime
import calendar
import json

class Termin:
    """
           Termin Klasse mit Titel, Datum und Zeit
           Returns
           -------
           object
           """
    def __init__(self, titel:str, date:str, time:str):
        """
        Kalendereinträge erstellen
        Datum, Zeit und Titel des Termins in Str.
        Returns
        -------
        object
        """
        self.titel = titel
        self.date_obj = datetime.strptime(date, "%d.%m.%Y").date() # Nimmt eingabe, wandelt es in Datumsinfo und extrahiert den Datumsanteil
        self.time_obj = datetime.strptime(time, "%H:%M").time()

    def __str__ (self):
        """
        Gibt eine lesbare String zurück. Ansonsten werden die Daten als Obj/Speicherort angezeigt.
        Returns
        -------
        object
        """
        datum_formatiert = self.date_obj.strftime("%d.%m.%Y")
        zeit_formatiert = self.time_obj.strftime("%H:%M")
        return f"{datum_formatiert} um {zeit_formatiert} Uhr: {self.titel}"

    def to_dict(self):
        """
        Wandelt den Termin in ein Json dict um
        Returns
        -------
        object
        """
        return {
            "titel": self.titel,
            "datum": self.date_obj.strftime("%d.%m.%Y"),
            "zeit": self.time_obj.strftime("%H:%M"),
        }

    @staticmethod # Hilft damit eine normale Funktion innerhalb des Klassenkontextes genutzt werden kann, ohne ein Objekt erstellen zu müssen
    def from_dict(data: dict):
        """
        Erstellt Termin aus dic
        -------
        object
        """
        return Termin(
            data["titel"],
            data["datum"],
            data["zeit"]
        )

class Kalender:
    def __init__(self, datei="termine.json"):
        """
        Erstelle ein leeres Obj für Termine.
        Returns
        -------
        object
        """

        self.termine = []
        self.datei = datei
        self.laden()

    def hinzufuegen(self):
        """
        Einen neuen Termin hinzufügen. Abfrage Datum, Zeit, Titel und auf leeren str einfügen.
        Greift auf Klasse Termin zu.
        Returns
        -------
        object
        """
        print("Neuen Termin erstellen")
        datum = input("Datum in TT.MM.JJJJ: ")
        zeit = input("Zeit in HH:MM: ")
        titel = input("Titel eingeben: ")

        try:
            neuer_termin = Termin(titel, datum, zeit)
            self.termine.append(neuer_termin)
            self.speichern()
            print(f"Termin {titel} wurde fuer den {datum} hinzugefügt.")
        except ValueError:
            # Fängt Fehler ab, wenn das Datum/Zeit-Format falsch ist
            print("Fehler: Ungültiges Datums- oder Zeitformat. Bitte TT.MM.JJJJ bzw. HH:MM verwenden.")

    def loeschen(self):
        """
        Rufe Anzeige aus.
        Frage nach der Nummer (Index + 1) des zu löschenden Termins
        Sortiere ungültige antworten aus
        Konvertiere die Eingabe in eine Ganzzahl und prufe ob der Index gültig ist
        Lösche index mit pop
        Returns
        -------
        object
        """
        if not self.termine:
            print("Keine Termine vorhanden")
            return

        self.anzeigen()

        # Frage nach der Nummer (Index + 1) des zu löschenden Termins
        auswahl = input("Welchen Termin wollen Sie löschen (Nummer eingeben, 0 zum Abbrechen): ")

        if auswahl == "0" or auswahl == "":
            print("Löschen abgebrochen.\n")
            return

        try:
            # Konvertiert eingabe in eine Ganzzahl
            index_zum_loeschen = int(auswahl) - 1

            # Prüfe, ob der Index gültig ist
            if 0 <= index_zum_loeschen < len(self.termine):
                geloeschter_termin = self.termine.pop(index_zum_loeschen)
                self.speichern()
                print(f"Termin {geloeschter_termin.titel} wurde gelöscht.")
            else:
                print("Fehler: Ungültige Nummer. Bitte eine Nummer aus der Liste wählen.")

        except ValueError:
            print("Fehler: Bitte geben Sie eine gültige Zahl ein.")

    def anzeigen(self):
        """
        Überprüfe ob Termine vorhanden sind
        Sortiere Datum und Zeit mit der Lambda Funktion
        enumarate um eine Liste zu erstellen die durchnummeriert ist.
        Returns
        -------
        object
        """
        if not self.termine:
            print("Keine Termine vorhanden.")
            return

        # Sortiert den Tupel Termine nach Datum und Zeit
        self.termine.sort(key=lambda t: (t.date_obj, t.time_obj))

        print("\n--- Ihre Termine ---")
        # enumerate erzeugt aus einem iterable (z.B. Liste) enumerate Objekt bestehend aus Tupeln, deren erster Wert
        # jeweils durchnummeriert ist. Fängt mit 0 an, also + 1.
        for index, termin in enumerate(self.termine):
            print(f"[{index + 1}] {termin}")

    def kalender_anzeigen(self):
        #calender Modul verwenden
        try:
            jahr = int(input("Gebe das Jahr ein YYYY: "))
            monat = int(input("Und Monat 1-12: "))
            kal = calendar.month(jahr, monat)
            print(kal)
        except ValueError:
            print("Falsche Eingabe")

    def speichern(self, datei="termine.json"):
        """
        Speichert alle Termine in eine Json Datei.
        Returns
        -------
        object
        """
        daten = [t.to_dict() for t in self.termine] # erstelle eine Liste von Dic
        try:
            with open(datei, "w") as f: #Öffnet eine Datei im Schreibmodus
                json.dump(daten, f, indent=2) # Schreibt die Liste in daten in die Datei f
            print("Termine wurden in eine Json Datei gespeichert")
        except Exception as e:
            print("Fehler beim Speichern: ", e)

    def laden(self, datei="termine.json"):
        """
        Lade eine Json Datei
        Returns
        -------
        object
        """
        try:
            with open (datei, "r") as f: #readable
                daten = json.load(f)
                self.termine = [Termin.from_dict(t) for t in daten]
                print("Termine geladen")
        except FileNotFoundError:
            print("Keine Speicherdaten gefunden")
        except Exception as e:
            print("Fehler beim Laden", e)

    def menu(self):
        """
        Zeige Menü an und verarbeitet Benutzereingaben
        Returns: str: Objekt
        -------
        object
        """
        while True:
            print("\nKALENDER-APP")
            print("[1] Termin hinzufügen")  # append
            print("[2] Alle Termine anzeigen")  # for schleife
            print("[3] Termin löschen")
            print("[4] Kalenderansicht")  # input abfrage und calendar.month(theyear, themonth)
            print("[5] Beenden")

            try:
                wahl = int(input("\nWähle eine Option (1-5): "))

                if wahl == 1:
                    self.hinzufuegen()
                elif wahl == 2:
                    self.anzeigen()
                elif wahl == 3:
                    self.loeschen()
                elif wahl == 4:
                    self.kalender_anzeigen()
                elif wahl == 5:
                    print("Bye bye")
                    break
                else:
                    print("Bitte von 1 bis 5 auswählen!")
            except ValueError:
                print("Bitte eine Zahl von 1 bis 5 eingeben")


if __name__ == "__main__":
    start = Kalender()
    start.menu()