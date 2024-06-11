import random
import time
import sys
import json
import os
import pygame

def slow(text, delay=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def play_music(file, loop=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loop)

def fade_music_to_volume(target_volume, duration):
    current_volume = pygame.mixer.music.get_volume()
    increment = (target_volume - current_volume) / duration
    for i in range(duration):
        current_volume += increment
        pygame.mixer.music.set_volume(current_volume)
        time.sleep(1)


def play_sound(file, volume=2.0, loop=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loop)
    pygame.mixer.music.set_volume(volume)

def fadeout_music(time_ms):
    pygame.mixer.music.fadeout(time_ms)

def fadeout_sound(time_ms):
    pygame.mixer.music.fadeout(time_ms)

def slow_print(text, delay=0.07):
    lines = text.split('\t')
    for line in lines:
        slow(line, delay)
        sys.stdout.flush()
        input()
def slow_input(prompt, delay=0.07):
    slow_print(prompt, delay)
    return input("> ")
def slow_ascii(text, delay=0.001):
    lines = text.split('\n')
    for line in lines:
        slow(line, delay)
        sys.stdout.flush()
def display_ascii(file_path):
    try:
        with open(file_path, 'r') as file:
            ascii_art = file.read()
            slow_ascii(ascii_art, delay=0.001)

    except FileNotFoundError:
        print("ASCII-Art-Datei nicht gefunden. Bitte stelle sicher, dass die Datei im richtigen Pfad existiert.")

class Player:
    def __init__(self, name):
        self.name = name
        self.epilog_path = None
        self.attributes = {
            "Empathie": 8,
            "Kondition": 8,
            "Geschicklichkeit": 8,
            "Kreativität": 8,
            "Charme": 8,
            "Intelligenz": 8,
            "Willensstärke": 8,
            "Neugier": 8,
            "Teamplayer": 8,
            "Mut": 8,
            "Freundlichkeit": 8,
            "Treue": 8
        }
        self.selected_attributes = {}

    def select_important_attributes(self):
        slow_print("Wähle drei Eigenschaften, von denen du denkst, dass sie am wichtigsten für dich sind:")
        available_attributes = list(self.attributes.keys())
        selected = 0
        slow_print("Verfügbare Eigenschaften:")
        for attribute in available_attributes:
            print(f"- {attribute}")
        while selected < 3:
            choice = slow_input(f"Wähle Eigenschaft {selected + 1}: ").strip()
            if choice in self.selected_attributes:
                slow_print("Das hast du schon ausgewählt, wähle etwas anderes.")
            elif choice in available_attributes:
                self.selected_attributes[choice] = self.attributes[choice] + 7  # Bonus von 2 auf die ausgewählten Eigenschaften
                available_attributes.remove(choice)
                selected += 1
            else:
                slow_print("Ungültige Auswahl. Bitte wähle eine gültige Eigenschaft.")

        for attribute in self.selected_attributes:
            self.attributes[attribute] = self.selected_attributes[attribute]

        slow_print("Ob das so eine gute Auswahl war? Wir werden ja sehen wohin das führt. Ich fasse nochmal zusammen:")
        for attribute, value in self.selected_attributes.items():
            slow_print(f"{attribute}: {value}")

    def __str__(self):
        return (f"{self.name}'s Attributes:\n" +
                "\n".join([f"{attr}: {value}" for attr, value in self.attributes.items()]))

class Game:
    def __init__(self):
        self.player = None
        self.results = []
    def roll_d20(self):
        return random.randint(1, 20)

    def roll_d20_mod(self, attribute, basis_zielwert=10):
        # Bonus für gewählte Attribute festlegen
        bonus = 0

        # Prüfen, ob das Attribut gewählt wurde und den entsprechenden Bonus anwenden
        if attribute in self.player.selected_attributes:
            bonus = self.player.selected_attributes[attribute]
        else:
            bonus = basis_zielwert

        # Würfeln eines W20 (20-seitiger Würfel)
        wurf = random.randint(1, 20)
        zielwert = 20-bonus
        return wurf, zielwert
        # Überprüfen, ob der modifizierte Wurf den Zielwert erreicht oder übertrifft

    def save_game(self, filename="letzter_spielstand.json"):
        state = {
            "player": {
                "name": self.player.name,
                "attributes": self.player.attributes,
                "selected_attributes": self.player.selected_attributes
            },
            "results": self.results
        }
        try:
            with open(filename, 'w') as f:
                json.dump(state, f)
            slow_print(f"Spielstand wurde in {filename} gespeichert.")
        except Exception as e:
            slow_print(f"Fehler beim Speichern des Spiels: {e}")
    def load_game(self, filename="letzter_spielstand.json"):
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
                self.player = Player(state["player"]["name"])
                self.player.attributes = state["player"]["attributes"]
                self.player.selected_attributes = state["player"]["selected_attributes"]
                self.results = state["results"]
            slow_print(f"Spielstand wurde aus {filename} geladen.")
        except FileNotFoundError:
            slow_print("Speicherdatei nicht gefunden. Ein neues Spiel wird gestartet.")
            self.start_new_game()

    def prompt_save_game(self):
        choice = slow_input("Möchtest du den aktuellen Spielstand speichern? \n1: Ja\n2: Nein ")
        if choice == "1" or choice == "Ja":
            self.save_game()

    def start_new_game(self):
        if os.path.exists("letzter_spielstand.json"):
            choice = slow_input(
                "Es wurde ein gespeicherter Spielstand gefunden. Möchtest du diesen laden?\n1: Ja\n2: Nein")
            if choice == "1" or choice == "Ja":
                self.load_game()
                self.epilog()
                return
        pygame.mixer.init()
        play_music("ÓlafurArnalds.mp3")
        slow_print(
            "******************************************* Doc Nuy Studios presents ************************************",
            delay=0.07)
        display_ascii("Boje.txt")
        slow_print("Willkommen Abenteurer", delay=0.07)
        while True:
            name = slow_input("Bitte gib deinen Namen ein: ")
            if not name.strip():
                slow_print("Ungeduldig? Ohne Namen geht's nicht weiter.")
            else:
                break

        if name != "Boje":
            slow_print(f"Na, ob {name} wohl dein richtiger Name ist? ;)")
        else:
            slow_print(f"Nicht Eragon? Na gut, dann {name}")
        self.player = Player(name)
        while True:
            bereit = slow_input("Bist du bereit? \n1: Ja\n2: Nein ").strip().lower()
            if bereit == "ja" or bereit == "1":
                slow_print("Nichts Geringeres habe ich erwartet.")
                break
            elif bereit == "nein" or bereit == "2":
                slow_print("Ich spiele mal die kleinste Violine der Welt für dich. Wir legen jetzt los.")
                break
            else:
                slow_print(f"{bereit} gibt's nicht! Bitte antworte mit 'Ja' oder 'Nein'.")

        self.player.select_important_attributes()
        self.prompt_save_game()
        fadeout_music(5000)
        self.epilog()

    def epilog(self):
        pygame.mixer.init()
        play_music("ÓlafurArnalds.mp3")
        display_ascii("Epilog.txt")
        slow_print("Du nimmst einen langen, ruhigen Atemzug und schaust dich um. Das Wasser um dich herum ist glasklar und kühl, ")
        slow_print("die Strahlen der Sonne brechen durch die Oberfläche und malen tanzende Muster auf den sandigen Meeresboden.")
        slow_print("Du bist 14 Meter unter der Wasseroberfläche, schwerelos schwebend, umgeben von einer fast magischen Stille.")
        slow_print("Deine Bewegungen sind langsam und mühelos. Blasen steigen beim Ausatmen aus deinem Atemregler auf und ")
        slow_print("du kannst dem Drang nicht widerstehen einen Blasenring zu erzeugen.")
        # Probe, ob der Blasenring gelingt
        wurf, zielwert = self.roll_d20_mod("Geschicklichkeit")
        slow_print(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.")
        if wurf >= zielwert:
            slow_print(
                "Erfolg! Mit einer geschickten Bewegung formst du einen perfekten Blasenring, der sich in der Weite des Meeres verliert. Eine deiner leichtesten Übungen.")
        else:
            slow_print("Misserfolg! Der Blasenring zerfällt, bevor er entsteht.")

        slow_print("Unvermittelt gleitet deine Hand an deinen Hals und greift:")
        # Weitere Probe
        wurf, zielwert = self.roll_d20_mod("Treue")
        slow_print(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.")
        self.results.append(wurf)

        if wurf >= zielwert:
            slow_print("Erfolg! Deinen Anhänger")
            self.schoener_traum()
        else:
            slow_print("Misserfolg! Nichts")
            self.alptraum()

    def alptraum(self):
        slow_print("Ein Schreck durchzuckt dich, als du deinen Anhänger nicht mehr fühlst. Wo ist er hin?")
        slow_print(
            "Panik überkommt dich, während du dich hektisch umsiehst und mit zitternden Händen nach dem vertrauten Kleinod tastest.")
        slow_print(
            "Du bist dir sicher, dass du ihn hier verloren haben musst. Entschlossen tauchst du tiefer, obwohl die Dunkelheit dichter wird.")
        slow_print(
            "Plötzlich hörst du ein leises Rascheln, ähnlich dem Geräusch von Pappelblättern, die im Wind tanzen.")
        slow_print(
            "Die Sicht wird schlechter und du kannst nicht erkennen, was dieses unheimliche Geräusch verursacht.")
        slow_print(
            "Ein Gefühl der Beklemmung überkommt dich. Dann, ohne Vorwarnung, wirst du heftig von etwas getroffen, als ob eine Salve von Paintballkugeln dich trifft.")
        slow_print(
            "Ein brennender Schmerz durchzuckt deinen Körper, als du realisierst, dass kleine Füsiliere durchs Wasser schießen und dich rammen.")
        slow_print(
            "Inmitten des Chaos wird dir klar: Sie fliehen vor etwas. Etwas Größerem, das jetzt auf dich zukommt...")
        choice = slow_input("Du musst schnell handeln. Was machst du? \n1: Es ist dir egal, du willst deinen Anhänger zurück und tauchst tiefer \n2: Du solltest den Fischen hinterherschwimmen und ebenfalls fliehen ")
        if choice == "1":
            fadeout_music(2000)
            play_music("Wild.mp3")
            slow_print("Du tauchst immer tiefer und verlierst den Sinn für das was du tust. Du bemerkst nur beiläufig wie dein Blickfeld immer schmaler wird. "
                       "Ist das der Tiefenrausch von dem immer gesprochen wurde? Plötzlich wird alles schwarz.")
            slow_print("Du schreckst auf!")
            self.epilog_path = "alptraum_tiefenrausch"
            fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()
        elif choice == "2":
            slow_print("Du folgst dem Schwarm mit kräftigen Flossenschlägen. Auch wenn du an die Geschwindigkeit des Fischschwarms nicht annähernd herankommst findest du den Zielort der Fische.")
            slow_print("Eine Felswand, in der es eine Höhle gibt")
            slow_print("Du entscheidest hineinzuschwimmen.")
            slow_print(
                "Die Wände der Höhle scheinen im schwachen Licht fast zu leuchten, und jede Bewegung im Wasser lässt es glitzern. Die Höhle ist voll von Leuchtalgen. Es fühlt sich an als hättest du einen vergessenen Ort betreten, den kaum jemand zuvor gesehen hat.")
            slow_print(
                "Du entdeckst bizarre Felsformationen, die wie Skulpturen aussehen.")
            slow_print("Für einen Moment vergisst du deine Angst und genießt die Schönheit dieses verborgenen Ortes.")
            slow_print("Doch langsam wird die Dunkelheit dichter und du schaust auf dein Finimeter...du hast nur noch 20 bar Luft in deinem Tank.")
            slow_print(
                "Du schaust dich um und hast keine Ahnung mehr wo du dich befindest. Doch dann scheint es, als würdest du die Wasseroberfläche über dir sehen. Hoffnung keimt in dir auf, und du schwimmst verzweifelt in diese Richtung.")
            fadeout_music(5000)
            play_music("Wild.mp3")
            slow_print(
                "Doch als du näher kommst, siehst du, dass es nur eine Blasenreflektion an der Höhlendecke ist, eine typische Illusion in solchen Tiefen.")
            slow_print(
                "Die Erkenntnis trifft dich hart, du wirst hier ertrinken... Auch wenn du weiter nach einem Ausweg suchst... irgendwann entweicht dein letzter Atemzug deinen Lungen, und alles um dich herum wird schwarz.")
            slow_print(
                "......................................................................Du schreckst hoch")
            self.epilog_path = "alptraum_höhle"
            fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()

        else:
            slow_print("Ungültige Wahl.")
            self.alptraum()

    def schoener_traum(self):
        slow_print(
            "Auf eine bizarre Art und Weise bist du erleichtert. Dein Herzschlag, der kurz aussetzte, findet seinen langsamen, stetigen Rhythmus wieder.")
        slow_print(
            "Du nimmst wieder deine Umgebung genauer wahr. Das Wasser ist so glasklar, dass es fast scheint, als könntest du mehrere Dutzend Meter weit sehen, auch wenn du weißt, dass das unmöglich ist.")
        slow_print("Während du weiter durch das Wasser gleitest, bemerkst du einen Schwarm Füsiliere.")
        slow_print(
            "Der Schwarm blitzt in Blau und Gelb von den glänzenden Schuppen und schwimmt auf dich zu. Ganz ruhig umkreisen sie dich und bilden bald eine schützende Kugel um dich.")
        slow_print("Egal in welche Richtung du blickst, überall sind diese kleinen Fische zu sehen.")
        while True:
            choice = slow_input(
                "Was tust du? \n1: Natürlich nach deinem Fisch suchen \n2: Natürlich nach deinem Divebuddy sehen \n3: Du versuchst dich zu orientieren: ").lower()
            if choice == "1":
                self.papageifisch_entdecken()
                break
            elif choice == "2":
                self.divebuddy_entdecken()
                break
            elif choice == "3":
                self.dich_orientieren()
                break
            else:
                slow_print("Ungültige Wahl.")

    def papageifisch_entdecken(self):
        slow_print("Dein Papageifisch den du liebevoll Norbert getauft hast, begleitet dich häufig auf deinen Tauchgängen und auch jetzt schwimmt er stoisch auf dich zu mit einer Muschel im Schnabel.")
        wurf, zielwert = self.roll_d20_mod("Teamplayer")
        slow_print(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.")
        self.results.append(wurf)
        if wurf >= zielwert:
            slow_print("Erfolg! Norbert gleitet an den anderen Fischen vorbei und stört die Sphäre nicht.")
            slow_print("Der dichte Schwarm nimmt dir dadurch die Sicht auf alles was um dich herum geschieht.")
            self.muschel_auffangen()
        else:
            slow_print("Misserfolg! Der positiv verstrahlte Norbert zerstört die perfekte Sphäre.")
            self.muschel_auffangen()

    def muschel_auffangen(self):
        slow_print("Deine Aufmerksamkeit richtet sich völlig auf den kleinen Norbert.")
        slow_print("Der Fisch schwimmt verspielt, um deine weißen Flossen und hinauf zu deiner Maske und lässt dann vor deinen Augen von der Muschel ab.")
        slow_print("Du streckst deine Hand durch das angenehm kühle Wasser und versuchst nach der Muschel zu greifen.")
        wurf, zielwert = self.roll_d20_mod("Geschicklickeit")
        slow_print(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.")
        self.results.append(wurf)
        if wurf >= zielwert:
            self.muschel_gefangen()
        else:
            self.muschel_verloren()

    def muschel_gefangen(self):
        slow_print("Erfolg! Du fängst die Muschel auf.")
        slow_print("Du betrachtest das Gebilde genauer, eine typische Koh Tao Shell, wie du sie damals von Justus geschenkt bekommen hast.")
        slow_print("Und du erkennst, dass etwas eigenartig an ihr ist... es steht etwas auf ihr geschrieben ...")
        wurf, zielwert = self.roll_d20_mod("Intelligenz")
        slow_print(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.")
        self.results.append(wurf)
        if wurf >= zielwert:
            slow_print("Erfolg! Du hältst die Muschel näher an deine Maske und der vergrößernde Effekt des Wassers hilft dir, die Schrift zu entziffern. "
                       "Die Antwort auf all deine Fragen ist... 42.... 42? Ist das ein Scherz? Du schaust zu Norbert, der dich bestärkend anzunicken scheint..."
                        "Definitiv ist das ein Scherz, denn dies ist ein Traum und du erwachst.")
            self.prompt_save_game()
            fadeout_music(3000)
            self.epilog_path = "traum_papagei_muschel_42"
            self.chapter1()
        else:
            slow_print(
                "Misserfolg! Du verbringst gefühlt Stunden damit herauszufinden, was dort stehen könnte, aber du schaffst es nicht. Völlig frustriert stellst du fest, dass du träumst...  Und du wachst auf.")
            self.epilog_path = "traum_Muschel"
            fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()
    def muschel_verloren(self):
        slow_print("Misserfolg! Du kannst die Muschel nicht fangen und sie sinkt in die Tiefe.... du versuchst erneut nachzugreifen, doch ein Ruck durchfährt dich... Und du wachst auf.")
        self.epilog_path = "traum_Muschel_verloren"
        self.prompt_save_game()
        fadeout_music(3000)
        self.chapter1()
    def divebuddy_entdecken(self):
        buddy_name = slow_input("Bitte gib den Namen deines Divebuddys ein: ")
        if buddy_name.lower() == "jule":
            self.special_event()
        else:
            slow_print(
                f"Du entdeckst deinen Tauchpartner {buddy_name} außerhalb der Fusiliersphäre und bemerkst, wie er/sie den Moment filmt.")
            slow_print(
                "Ein Gefühl der Erleichterung und Freude durchströmt dich – dieser magische Moment wird festgehalten.")
            slow_print(
                "Du verweilst noch eine Weile inmitten des schimmernden Schwarms, bis dein Buddy dir signalisiert, dass es weitergehen sollte.")
            wurf, zielwert = self.roll_d20_mod("Teamplayer")
            slow_print(f"Du machst eine Teamplayer-Probe : {wurf}.")
            if wurf >= zielwert:
                slow_print(
                    "Mit einem letzten widerstrebenden Blick löst du dich aus der schützenden Sphäre und tauchst langsam zu ihm/ihr hin.")
            else:
                slow_print(
                    "Du bleibst in der Sphäre, drehst dich um deine eigene Achse, immer immer wieder, bis der Schwarm schnell um dich zu kreisen scheint, immer schneller..."
                    "und du erwachst.")
                self.epilog_path = "Buddy_Sphäre"
                fadeout_music(3000)
                self.prompt_save_game()
                self.chapter1()
            slow_print(
                "Mit einem letzten widerstrebenden Blick löst du dich aus der schützenden Sphäre und tauchst langsam zu ihm/ihr hin.")
            slow_print("Er/sie zeigt dir das Video auf der Kamera und ein Lächeln breitet sich auf deinem Gesicht aus.")
            slow_print("Mit dem Bild des schimmernden Schwarms noch vor Augen... erwachst du.")
            self.epilog_path = "Buddy_Video"
            fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()
    def special_event(self):
        slow_print("Du siehst wie Jule in einer komplett umgekehrten Orientierung zu dir halb in einem eigenen Schwarm von Fischen schwebt und dir fröhlich zuwinkt.")
        slow_print("Du bist kurz verwirrt, weil dir nicht klar ist, wer von euch jetzt kopfüber schwimmt.")
        wurf, zielwert = self.roll_d20_mod("Intelligenz")
        slow_print(f"Du machst eine Intelligenz-Probe : {wurf}.")
        if wurf >= zielwert:
            slow_print("Erfolg! Du legst deinen Kopf schief und während du dir noch darüber klar wirst, wo nun oben und unten ist, beobachtest du amüsiert, wie Jule plötzlich jubelnde Gesten macht und dir bedeutet herzuschwimmen.")
            self.walhai_event()
        else:
            slow_print("Misserfolg! Du legst deinen Kopf schief und während du dir noch darüber klar wirst, wo nun oben und unten ist, beobachtest du leicht genervt, wie Jule plötzlich jubelnde Gesten macht und dir bedeutet herzuschwimmen. Zeigt sie dir nun die 100. Felsformation, die wie ein Gesicht aussieht?")
            self.walhai_event()

    def walhai_event(self):
        wurf, zielwert = self.roll_d20_mod("Empathie")
        slow_print(f"Du machst eine Empathie-Probe : {wurf}.")
        if wurf >= zielwert:
            slow_print("Erfolg! Du entscheidest dich zu ihr zu schwimmen"
                        "Jule freut sich sichtlich, dass du entschlossen hast, deine kleine Sphäre zu verlassen."
                        "Sie zeigt dir das Zeichen für Walhai und du musst loslachen, du denkst dass sie dich hochnehmen will. Wäre ja nicht das erste mal. Du tippst mit deinem Zeigefinger an deine Schläfe."
                        "Du kannst sogar durch die Maske Jules hochgezogene Augenbraue sehen, während sie den Kopf schüttelt und dann beginnt voranzuschwimmen. Du folgst ihr und tatsächlich erkennst du einen dunklen Schatten einige Meter entfernt von euch."
                        "Ihr entschließt euch näher zu schwimmen und werdet belohnt. Ein Walhai gleitet über euch hinweg und saugt eine große Menge Plankton ein. Ihr beobachtet eine gefühlte Ewigkeit, wie der Meeresriese durch das Wasser gleitet."
                        "Dann reißt dich ein Schwall Blasen aus deiner Trance und eigenartigerweise hörst du Jules schmunzelnde Stimme: Schade dass es nur ein Traum ist oder?"
                        "Du schaust dich irritiert zu ihr um und .... erwachst.")
            self.epilog_path = "Special_Walhai"
            fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()

        else:
            slow_print("Misserfolg! Bleibst in deiner Sphäre")
            slow_print("Jule ist sichtlich nicht sehr begeistert darüber, dass du dich nicht von Ort und Stelle bewegst, entschließt sich aber, dich nicht allein zu lassen und schwimmt zu dir herüber.")
            slow_print("Als sie die Sphäre erreicht, kannst du ihre schmunzelnde Stimme in deinem Kopf hören: Du bist so ein Vollpfosten. "
                       "Du musst lachen und .... wachst auf.")
            self.epilog_path = "Special_Vollpfosten"
            self.prompt_save_game()
            fadeout_music(3000)
            self.chapter1()

    def dich_orientieren(self):
        slow_print("Du orientierst dich und hast zunächst wirklich nicht die leiseste Ahnung, wo du bist.")
        wurf, zielwert = self.roll_d20_mod("Intelligenz")
        slow_print(f"Du würfelst eine {wurf}.")
        if wurf >= zielwert:
            self.navigieren()
        else:
            slow_print("Misserfolg! Navigation ist nicht so deine Stärke was? Nach einer Weile entschließt du dich langsam aufzutauchen und sobald du die Wasseroberfläche durchbrochen hast, "
                       "wachst du auf.")
            self.epilog_path = "orientieren_fail"
            self.prompt_save_game()
            fadeout_music(3000)
            self.chapter1()

    def navigieren(self):
        slow_print("Erfolg! Du weißt zwar nicht wo du bist, aber deine Sinne beginnen sich zu schärfen und du beginnst zu lauschen. Und tatsächlich, du hörst ein charakteristisches Brummen von Tönen… .")
        fade_music_to_volume(0.1, duration=3)
        play_sound("Morse.mp3", volume=2.0)
        choice = slow_input(
            "Weißt du was die Nachricht bedeutet? \n1: Na klar, bin ja nicht von gestern. \n2: Nein, ich brauche einen Telefonjoker. ").lower()
        if choice == "1":
            fadeout_sound(3000)
            fade_music_to_volume(1, duration=3)
            play_music("ÓlafurArnalds.mp3")
            correct_sequence = [
                ("n", 20), ("w", 25), ("n", 20), ("o", 24),
                ("n", 100), ("w", 50), ("n", 20), ("o", 5)
            ]
            input_sequence = []
            direction_descriptions = {
                "n": [
                    f"Du schwimmst nach Norden durch eine dichte Seegraswiese.",
                    f"Du tauchst in nördlicher Richtung zwischen hoch aufragenden Korallenbänken hindurch.",
                    f"Nach Norden schwimmend, findest du eine Gruppe neugieriger Fische."
                ],
                "w": [
                    f"Du schwimmst nach Westen entlang eines Korallenriffs.",
                    f"Im Westen durchquerst du ein Feld farbenfroher Anemonen.",
                    f"Nach Westen gleitest du an einem versunkenen Schiffswrack vorbei."
                ],
                "o": [
                    f"Du schwimmst nach Osten durch klares, Blauwasser.",
                    f"Im Osten siehst du eine geheimnisvolle Höhle in der Ferne.",
                    f"Du tauchst  nach Osten und entdeckst einen alten, verrosteten Anker."
                ]
            }

            for direction, distance in correct_sequence:
                dir_input = slow_input(f"In welche Richtung geht es? ").strip().lower()
                dist_input = slow_input(f"Wie viele Meter?").strip()
                try:
                    dist_input = int(dist_input)
                except ValueError:
                    slow_print("Ungültige Eingabe. Bitte versuche es erneut.")
                    break  # Falls eine Eingabe ungültig ist, zum Anfang der Schleife zurückkehren

                input_sequence.append((dir_input, dist_input))

                if dir_input in direction_descriptions:
                    description = random.choice(direction_descriptions[dir_input])
                    slow_print(description)
            if input_sequence == correct_sequence:
                slow_print("Du bist dir sehr sicher, dass du den Anweisungen genau gefolgt bist und schaust dich am Zielort um und du findest tatsächlich eine klischeehafte Holzkiste. Du hast einen Schatz gefunden!")
                self.looten()
            else:
                slow_print("Falsche Eingabe. Du musst zum Anfang der Sequenz zurückkehren.")
        elif choice == "2":
            slow_print("Du hörst weiter zu...")

    def looten(self):
        slow_print("Du schaust nochmal auf deine Tauchuhr, siehst deinen Schwimmverlauf und fühlst dich ein wenig verarscht, aber dass du eine Schatzkiste gefunden hast, macht den kurz aufkommenden Ärger wieder wett.")
        slow_print("Beinahe zu deiner Enttäuschung siehst du dass die Schatzkiste nicht mit einem Schloss verschlossen ist und öffnest sie. Du findest in der Schatzkiste eine grüne Brille, ein Tagebuch und einen Griff.")
        slow_print("Dein Inventar wurde um >> Der widerhallende Griff << >>Die Brille des smaragdgrünen Blicks<< und das  >>Buch der Mythen<< erweitert")
        slow_print("Alles kommt dir bekannt vor, was machen diese Gegenstände in der Kiste? Du nimmst dir das Buch und als du hindurch blätterst scheint alles so wie immer, aber eine Seite ganz am Ende zeigt dir etwas neues: Du schaust hin und liest: Wach auf!")
        slow_print("Und du wachst auf.")
        self.epilog_path = "Orientieren_success"
        self.prompt_save_game()
        fadeout_music(3000)
        self.chapter1()

    def chapter1(self):
        play_music("theory.mp3")
        slow_print("Du erwachst in deinem Bett.")
        slow_print("........................................................................................\n"
                    "..............................Hier entsteht Chapter1....................................\n"
                    "...................................Deine Reise..........................................\n"
                    "........................................................................................\n"
                    "Danke, fürs Zocken!\n"
                    "Entwickler: Jule\n"
                    "Skript: Auch Jule\n"
                    "Design: Immer noch Jule\n"
                    "Musik: :D \n"
                    "Entwickelt für Boje und gewidmet seinem Eintritt in die epischen Dreißiger ;)")

        #display_ascii("")
        ####if self.epilog_path == "schoener_traum":
        ###    slow_print("Nach deinem erholsamen Traum wachst du mit einem Gefühl der Zufriedenheit auf.")
        ###elif self.epilog_path == "alptraum":
       ###     slow_print("Du wachst mit einem Schreck auf, dein Herz rast immer noch von dem Alptraum.")
        ###else:
        ###    slow_print("Du erwachst ohne besondere Erinnerung an den Traum.")




if __name__ == "__main__":
    game = Game()
    game.start_new_game()

