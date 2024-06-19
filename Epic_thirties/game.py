import random
import subprocess
import time
import sys
import json
import os
import pygame
import queue
from typing import List, Tuple, Literal, Union


class Game:
    def __init__(self):
        # Initialize pygame and font
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Consolas", 17)
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption('Epic 30s')

        self.main_event_queue = queue.Queue()
        self.player = None
        self.results = []
        self.epilog_path = None  # Hier wird epilog_path definiert
        self.rendered_text = []  # Initialisiere gerenderten Text als Liste
        self.scroll_offset = 0  # Scroll-Offset

    def render_text_to_screen(self, text=None):
        self.screen.fill((0, 0, 0))
        y_offset = (self.screen.get_height() // 2) - self.scroll_offset
        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width() - 100  # Adjust width for padding

        if text:
            lines_to_render = [text]
        else:
            lines_to_render = self.rendered_text

        for line in lines_to_render:
            wrapped_lines = self.wrap_text(line, screen_width)
            for wrapped_line in wrapped_lines:
                rendered_line = self.font.render(wrapped_line, True, (255, 255, 255))
                if y_offset + rendered_line.get_height() <= screen_height:
                    self.screen.blit(rendered_line, (50, y_offset))
                y_offset += self.font.get_height()  # Abstand zwischen den Zeilen verringern
        pygame.display.flip()

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = f'{current_line} {word}'.strip()
            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        return lines

    def print_text(self, text, delay=0.01, wait_after=False):
        for char in text:
            if char == '\n':
                if not self.rendered_text or self.rendered_text[-1] != "":
                    self.rendered_text.append("")
            else:
                if not self.rendered_text or self.rendered_text[-1] == "":
                    self.rendered_text.append(char)
                else:
                    self.rendered_text[-1] += char
            self.render_text_to_screen()
            pygame.time.delay(int(delay * 1000))
        self.render_text_to_screen()
        self.auto_scroll_to_bottom()
        if wait_after:
            self.wait_for_enter()

    def auto_scroll_to_bottom(self):
        # Scroll to bottom to keep the prompt visible
        total_text_height = len(self.rendered_text) * self.font.get_height()
        visible_height = self.screen.get_height() - 100  # Adjust to leave some space at the bottom
        self.scroll_offset = max(0, total_text_height - visible_height)
        self.render_text_to_screen()

    def slow_input(self, prompt) -> str:
        self.print_text(prompt)
        user_input = ""
        if self.rendered_text and self.rendered_text[-1] == "":
            self.rendered_text.pop()
        self.rendered_text.append("")
        self.rendered_text.append("> ")  # Prompt anzeigen
        self.render_text_to_screen()
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evt.type == pygame.KEYDOWN:
                    if evt.key == pygame.K_RETURN:
                        self.rendered_text.append("")  # Neue Zeile nach der Eingabe
                        self.auto_scroll_to_bottom()
                        return user_input
                    elif evt.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += evt.unicode
                    # Aktualisiere die letzte Zeile in rendered_text mit dem aktuellen user_input
                    self.rendered_text[-1] = "\n> " + user_input
                    self.render_text_to_screen()
                elif evt.type == pygame.MOUSEBUTTONDOWN:
                    if evt.button == 4:  # Scroll up
                        self.scroll_offset = max(self.scroll_offset - 30, 0)
                    elif evt.button == 5:  # Scroll down
                        total_text_height = len(self.rendered_text) * self.font.get_height()
                        visible_height = self.screen.get_height() - 50
                        self.scroll_offset = min(self.scroll_offset + 30, max(0, total_text_height - visible_height))
                    self.render_text_to_screen()

    def get_literal_direction(self, input_str: str) -> Union[Literal['n'], Literal['w'], Literal['o']]:
        if input_str == 'n':
            return 'n'
        elif input_str == 'w':
            return 'w'
        elif input_str == 'o':
            return 'o'
        else:
            raise ValueError("Invalid direction")

    def play_music(self, file, loop=-1):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loop)

    def fade_music_to_volume(self, target_volume, duration):
        current_volume = pygame.mixer.music.get_volume()
        increment = (target_volume - current_volume) / duration
        for i in range(duration):
            current_volume += increment
            pygame.mixer.music.set_volume(current_volume)
            time.sleep(1)

    def play_sound(self, file, volume=2.0, loop=-1):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loop)
        pygame.mixer.music.set_volume(volume)

    def fadeout_music(self, time_ms):
        pygame.mixer.music.fadeout(time_ms)

    def fadeout_sound(self, time_ms):
        pygame.mixer.music.fadeout(time_ms)

    def display_ascii(self, file_path, delay=0.01):
        try:
            with open(file_path, 'r') as file:
                ascii_art = file.read()
                lines = ascii_art.split('\n')
                for line in lines:
                    self.rendered_text.append(line)
                    pygame.time.delay(int(delay * 1000))
                self.render_text_to_screen()
        except FileNotFoundError:
            print("ASCII-Art-Datei nicht gefunden. Bitte stelle sicher, dass die Datei im richtigen Pfad existiert.")

    def wait_for_enter(self):
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_RETURN:
                    return

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
        zielwert = 20 - bonus
        self.wait_for_enter()
        return wurf, zielwert

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
            self.print_text(f"Spielstand wurde in {filename} gespeichert.")
        except Exception as e:
            self.print_text(f"Fehler beim Speichern des Spiels: {e}")

    def load_game(self, filename="letzter_spielstand.json"):
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
                self.player = Player(state["player"]["name"])
                self.player.attributes = state["player"]["attributes"]
                self.player.selected_attributes = state["player"]["selected_attributes"]
                self.results = state["results"]
            self.print_text(f"Spielstand wurde aus {filename} geladen.")
        except FileNotFoundError:
            self.print_text("Speicherdatei nicht gefunden. Ein neues Spiel wird gestartet.")
            self.start_new_game()

    def prompt_save_game(self):
        choice = self.slow_input("Möchtest du den aktuellen Spielstand speichern? \n1: Ja\n2: Nein\n")
        if choice == "1" or choice.lower() == "ja":
            self.save_game()

    def start_new_game(self):
        if os.path.exists("letzter_spielstand.json"):
            choice = self.slow_input(
                "Es wurde ein gespeicherter Spielstand gefunden. \n Möchtest du diesen laden?\n1: Ja\n2: Nein\n")
            if choice == "1" or choice.lower() == "ja":
                self.load_game()
                self.epilog()
                return
        pygame.mixer.init()
        self.play_music("ÓlafurArnalds.mp3")
        self.print_text(
            "************************************* Doc Nuy Studios presents ********************************")
        self.display_ascii("Boje.txt")
        self.print_text("Willkommen Abenteurer\n")
        while True:
            name = self.slow_input("Bitte gib deinen Namen ein: \n")
            if not name.strip():
                self.print_text("Ungeduldig? Ohne Namen geht's nicht weiter.\n")
            else:
                break

        if name != "Boje":
            self.print_text(f"Na, ob {name} wohl dein richtiger Name ist? ;)\n")
        else:
            self.print_text(f"Nicht Eragon? Na gut, dann {name}\n")
        self.player = Player(name)
        while True:
            bereit = self.slow_input("Bist du bereit? \n1: Ja\n2: Nein\n").strip().lower()
            if bereit == "ja" or bereit == "1":
                self.print_text("Nichts Geringeres habe ich erwartet.\n")
                break
            elif bereit == "nein" or bereit == "2":
                self.print_text("Ich spiele mal die kleinste Violine der Welt für dich. Wir legen jetzt los.\n")
                break
            else:
                self.print_text(f"{bereit} gibt's nicht! Bitte antworte mit 'Ja' oder 'Nein'.\n")

        self.player.select_important_attributes()
        self.prompt_save_game()
        self.fadeout_music(5000)
        self.epilog()

    def epilog(self):
        pygame.mixer.init()
        self.play_music("ÓlafurArnalds.mp3")
        self.display_ascii("Epilog.txt")
        self.print_text(
            "Du nimmst einen langen, ruhigen Atemzug und schaust dich um. Das Wasser um dich herum ist glasklar\n und kühl,")
        self.print_text(
            "die Strahlen der Sonne brechen durch die Oberfläche und malen tanzende Muster auf den \nsandigen Meeresboden.", wait_after= True)
        self.print_text(
            "Du bist 14 Meter unter der Wasseroberfläche, schwerelos schwebend, umgeben \nvon einer fast magischen Stille.", wait_after= True)
        self.print_text(
            "Deine Bewegungen sind langsam und mühelos. Blasen steigen beim Ausatmen aus \n deinem Atemregler auf und ")
        self.print_text("du kannst dem Drang nicht widerstehen einen Blasenring zu erzeugen.", wait_after= True)
        # Probe, ob der Blasenring gelingt
        wurf, zielwert = self.roll_d20_mod("Geschicklichkeit")
        self.print_text(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.", wait_after=True)
        if wurf >= zielwert:
            self.print_text(
                "Erfolg! Mit einer geschickten Bewegung formst du einen perfekten Blasenring, \nder sich in der Weite des Meeres verliert. Eine deiner leichtesten Übungen.", wait_after=True)
        else:
            self.print_text("Misserfolg! Der Blasenring zerfällt, bevor er entsteht.", wait_after=True)

        self.print_text("Unvermittelt gleitet deine Hand an deinen Hals und greift:", wait_after=True)
        # Weitere Probe
        wurf, zielwert = self.roll_d20_mod("Treue")
        self.print_text(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.", wait_after=True)
        self.results.append(wurf)

        if wurf >= zielwert:
            self.print_text("Erfolg! Deinen Anhänger", wait_after=True)
            self.schoener_traum()
        else:
            self.print_text("Misserfolg! Nichts", wait_after=True)
            self.alptraum()

    def alptraum(self):
        self.print_text("Ein Schreck durchzuckt dich, als du deinen Anhänger nicht mehr fühlst. Wo ist er hin?\n")
        self.print_text(
            "Panik überkommt dich, während du dich hektisch umsiehst und mit zitternden Händen nach dem vertrauten Kleinod tastest.\n", wait_after=True)
        self.print_text(
            "Du bist dir sicher, dass du ihn hier verloren haben musst. Entschlossen tauchst du tiefer, obwohl die Dunkelheit dichter wird.\n")
        self.print_text(
            "Plötzlich hörst du ein leises Rascheln, ähnlich dem Geräusch von Pappelblättern, die im Wind tanzen.\n", wait_after=True)
        self.print_text(
            "Die Sicht wird schlechter und du kannst nicht erkennen, was dieses unheimliche Geräusch verursacht.\n")
        self.print_text(
            "Ein Gefühl der Beklemmung überkommt dich. Dann, ohne Vorwarnung, wirst du heftig von etwas getroffen, \nals ob eine Salve von Paintballkugeln dich trifft.\n", wait_after=True)
        self.print_text(
            "Ein brennender Schmerz durchzuckt deinen Körper, als du realisierst, dass kleine Füsiliere durchs Wasser schießen und dich rammen.\n", wait_after=True)
        self.print_text(
            "Inmitten des Chaos wird dir klar: Sie fliehen vor etwas. Etwas Größerem, das jetzt auf dich zukommt...\n", wait_after=True)
        choice = self.slow_input(
            "Du musst schnell handeln. Was machst du? \n1: Es ist dir egal, du willst deinen Anhänger zurück und tauchst tiefer \n2: Du solltest den Fischen hinterherschwimmen und ebenfalls fliehen. \n")
        if choice == "1":
            self.fadeout_music(2000)
            self.play_music("Wild.mp3")
            self.print_text(
                "Du tauchst immer tiefer und verlierst den Sinn für das was du tust. \nDu bemerkst nur beiläufig wie dein Blickfeld immer schmaler wird.", wait_after=True)
            self.print_text("Ist das der Tiefenrausch von dem immer gesprochen wurde? Plötzlich wird alles schwarz.\n", wait_after=True)
            self.print_text("Du schreckst auf!\n")
            self.epilog_path = "alptraum_tiefenrausch"
            self.fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()
        elif choice == "2":
            self.print_text(
                "Du folgst dem Schwarm mit kräftigen Flossenschlägen. Auch wenn du an die Geschwindigkeit des Fischschwarms nicht annähernd herankommst\n findest du den Zielort der Fische.\n", wait_after=True)
            self.print_text("Eine Felswand, in der es eine Höhle gibt\n")
            self.print_text("Du entscheidest hineinzuschwimmen.\n", wait_after=True)
            self.print_text(
                "Die Wände der Höhle scheinen im schwachen Licht fast zu leuchten, und jede Bewegung im Wasser lässt es glitzern.\n Die Höhle ist voll von Leuchtalgen. Es fühlt sich an als hättest du einen vergessenen Ort betreten, den kaum jemand zuvor gesehen hat.\n", wait_after=True)
            self.print_text(
                "Du entdeckst bizarre Felsformationen, die wie Skulpturen aussehen.\n")
            self.print_text(
                "Für einen Moment vergisst du deine Angst und genießt die Schönheit dieses verborgenen Ortes.\n")
            self.print_text(
                "Doch langsam wird die Dunkelheit dichter und du schaust auf dein Finimeter...du hast nur noch 20 bar Luft in deinem Tank.\n",wait_after= True)
            self.print_text(
                "Du schaust dich um und hast keine Ahnung mehr wo du dich befindest. Doch dann scheint es, als würdest du die Wasseroberfläche über dir sehen. \nHoffnung keimt in dir auf, und du schwimmst verzweifelt in diese Richtung.\n",wait_after= True)
            self.fadeout_music(5000)
            self.play_music("Wild.mp3")
            self.print_text(
                "Doch als du näher kommst, siehst du, dass es nur eine Blasenreflektion an der Höhlendecke ist, eine typische Illusion in solchen Tiefen.\n",wait_after= True)
            self.print_text(
                "Die Erkenntnis trifft dich hart, du wirst hier ertrinken... Auch wenn du weiter nach einem Ausweg suchst... irgendwann entweicht dein letzter Atemzug deinen Lungen,\n und alles um dich herum wird schwarz.\n",wait_after= True)
            self.print_text(
                "......................................................................Du schreckst hoch.\n")
            self.epilog_path = "alptraum_höhle"
            self.fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()

        else:
            self.print_text("Ungültige Wahl.",wait_after= True)
            self.alptraum()

    def schoener_traum(self):
        self.print_text(
            "Auf eine bizarre Art und Weise bist du erleichtert. Dein Herzschlag, der kurz aussetzte, findet seinen langsamen, stetigen Rhythmus wieder.\n",wait_after= True)
        self.print_text(
            "Du nimmst wieder deine Umgebung genauer wahr. Das Wasser ist so glasklar, dass es fast scheint, als könntest du mehrere Dutzend Meter weit sehen, \nauch wenn du weißt, dass das unmöglich ist.\n",wait_after= True)
        self.print_text("Während du weiter durch das Wasser gleitest, bemerkst du einen Schwarm Füsiliere.\n")
        self.print_text(
            "Der Schwarm blitzt in Blau und Gelb von den glänzenden Schuppen und schwimmt auf dich zu. Ganz ruhig umkreisen sie dich und bilden bald eine schützende Kugel um dich.\n",wait_after= True)
        self.print_text("Egal in welche Richtung du blickst, überall sind diese kleinen Fische zu sehen.\n",wait_after= True)
        while True:
            choice = self.slow_input(
                "Was tust du? \n1: Natürlich nach deinem Fisch suchen \n2: Natürlich nach deinem Divebuddy sehen \n3: Du versuchst dich zu orientieren: \n").lower()
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
                self.print_text("Ungültige Wahl.",wait_after= True)

    def papageifisch_entdecken(self):
        self.print_text(
            "Dein Papageifisch den du liebevoll Norbert getauft hast, begleitet dich häufig auf deinen Tauchgängen \nund auch jetzt schwimmt er stoisch auf dich zu mit einer Muschel im Schnabel.\n",wait_after= True)
        wurf, zielwert = self.roll_d20_mod("Teamplayer")
        self.print_text(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.",wait_after= True)
        self.results.append(wurf)
        if wurf >= zielwert:
            self.print_text("Erfolg! Norbert gleitet an den anderen Fischen vorbei und stört die Sphäre nicht.\n")
            self.print_text("Der dichte Schwarm nimmt dir dadurch die Sicht auf alles was um dich herum geschieht.\n",wait_after= True)
            self.muschel_auffangen()
        else:
            self.print_text("Misserfolg! Der positiv verstrahlte Norbert zerstört die perfekte Sphäre.\n",wait_after= True)
            self.muschel_auffangen()

    def muschel_auffangen(self):
        self.print_text("Deine Aufmerksamkeit richtet sich völlig auf den kleinen Norbert.\n")
        self.print_text(
            "Der Fisch schwimmt verspielt, um deine weißen Flossen und hinauf zu deiner Maske und lässt dann vor deinen Augen von der Muschel ab.\n")
        self.print_text(
            "Du streckst deine Hand durch das angenehm kühle Wasser und versuchst nach der Muschel zu greifen.\n",wait_after= True)
        wurf, zielwert = self.roll_d20_mod("Geschicklickeit")
        self.print_text(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.",wait_after= True)
        self.results.append(wurf)
        if wurf >= zielwert:
            self.muschel_gefangen()
        else:
            self.muschel_verloren()

    def muschel_gefangen(self):
        self.print_text("Erfolg! Du fängst die Muschel auf.\n")
        self.print_text(
            "Du betrachtest das Gebilde genauer, eine typische Koh Tao Shell, wie du sie damals von Justus geschenkt bekommen hast.\n")
        self.print_text("Und du erkennst, dass etwas eigenartig an ihr ist... es steht etwas auf ihr geschrieben ...\n",wait_after= True)
        wurf, zielwert = self.roll_d20_mod("Intelligenz")
        self.print_text(f"Du würfelst eine {wurf}. Zielwert ist {zielwert}.",wait_after= True)
        self.results.append(wurf)
        if wurf >= zielwert:
            self.print_text(
                "Erfolg! Du hältst die Muschel näher an deine Maske und der vergrößernde Effekt des Wassers hilft dir, die Schrift zu entziffern. \n "
                "Die Antwort auf all deine Fragen ist... 42.... 42? Ist das ein Scherz? Du schaust zu Norbert, der dich bestärkend anzunicken scheint...\n "
                "Definitiv ist das ein Scherz, denn dies ist ein Traum und du erwachst.\n",wait_after= True)
            self.prompt_save_game()
            self.fadeout_music(3000)
            self.epilog_path = "traum_papagei_muschel_42"
            self.chapter1()
        else:
            self.print_text(
                "Misserfolg! Du verbringst gefühlt Stunden damit herauszufinden, was dort stehen könnte, aber du schaffst es nicht. \nVöllig frustriert stellst du fest, dass du träumst...  Und du wachst auf.\n",wait_after= True)
            self.epilog_path = "traum_Muschel"
            self.fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()

    def muschel_verloren(self):
        self.print_text(
            "Misserfolg! Du kannst die Muschel nicht fangen und sie sinkt in die Tiefe.... \ndu versuchst erneut nachzugreifen, doch ein Ruck durchfährt dich... \nUnd du wachst auf.",wait_after= True)
        self.epilog_path = "traum_Muschel_verloren"
        self.prompt_save_game()
        self.fadeout_music(3000)
        self.chapter1()

    def divebuddy_entdecken(self):
        buddy_name = self.slow_input("Bitte gib den Namen deines Divebuddys ein: \n")
        if buddy_name.lower() == "jule":
            self.special_event()
        else:
            self.print_text(
                f"Du entdeckst deinen Tauchpartner {buddy_name} außerhalb der Fusiliersphäre und bemerkst, wie er/sie den Moment filmt.\n")
            self.print_text(
                "Ein Gefühl der Erleichterung und Freude durchströmt dich – dieser magische Moment wird festgehalten.\n")
            self.print_text(
                "Du verweilst noch eine Weile inmitten des schimmernden Schwarms, bis dein Buddy dir signalisiert, dass es weitergehen sollte.\n",wait_after= True)
            wurf, zielwert = self.roll_d20_mod("Teamplayer")
            self.print_text(f"Du machst eine Teamplayer-Probe : {wurf}.",wait_after= True)
            if wurf >= zielwert:
                self.print_text(
                    "Mit einem letzten widerstrebenden Blick löst du dich aus der schützenden Sphäre und tauchst langsam zu ihm/ihr hin.\n",wait_after= True)
            else:
                self.print_text(
                    "Du bleibst in der Sphäre, drehst dich um deine eigene Achse, immer immer wieder, bis der Schwarm schnell um dich zu kreisen scheint, immer schneller...\n"
                    "und du erwachst.",wait_after= True)
                self.epilog_path = "Buddy_Sphäre"
                self.fadeout_music(3000)
                self.prompt_save_game()
                self.chapter1()
            self.print_text(
                "Mit einem letzten widerstrebenden Blick löst du dich aus der schützenden Sphäre und tauchst langsam zu ihm/ihr hin.\n")
            self.print_text(
                "Er/sie zeigt dir das Video auf der Kamera und ein Lächeln breitet sich auf deinem Gesicht aus.\n",wait_after= True)
            self.print_text("Mit dem Bild des schimmernden Schwarms noch vor Augen... erwachst du.\n",wait_after= True)
            self.epilog_path = "Buddy_Video"
            self.fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()

    def special_event(self):
        self.print_text(
            "Du siehst wie Jule in einer komplett umgekehrten Orientierung zu dir halb in einem eigenen Schwarm von Fischen schwebt und dir fröhlich zuwinkt.\n")
        self.print_text("Du bist kurz verwirrt, weil dir nicht klar ist, wer von euch jetzt kopfüber schwimmt.\n",wait_after= True)
        wurf, zielwert = self.roll_d20_mod("Intelligenz")
        self.print_text(f"Du machst eine Intelligenz-Probe : {wurf}.",wait_after= True)
        if wurf >= zielwert:
            self.print_text(
                "Erfolg! Du legst deinen Kopf schief und während du dir noch darüber klar wirst, wo nun oben und unten ist, \n beobachtest du amüsiert, wie Jule plötzlich jubelnde Gesten macht und dir bedeutet herzuschwimmen.\n",wait_after= True)
            self.walhai_event()
        else:
            self.print_text(
                "Misserfolg! Du legst deinen Kopf schief und während du dir noch darüber klar wirst, wo nun oben und unten ist, \n beobachtest du leicht genervt, wie Jule plötzlich jubelnde Gesten macht und dir bedeutet herzuschwimmen.\n Zeigt sie dir nun die 100. Felsformation, die wie ein Gesicht aussieht?\n",wait_after= True)
            self.walhai_event()

    def walhai_event(self):
        wurf, zielwert = self.roll_d20_mod("Empathie")
        self.print_text(f"Du machst eine Empathie-Probe : {wurf}.",wait_after= True)
        if wurf >= zielwert:
            self.print_text("Erfolg! Du entscheidest dich zu ihr zu schwimmen\n"
                            "Jule freut sich sichtlich, dass du entschlossen hast, deine kleine Sphäre zu verlassen.\n"
                            "Sie zeigt dir das Zeichen für Walhai und du musst loslachen, du denkst dass sie dich hochnehmen will. \nWäre ja nicht das erste mal. Du tippst mit deinem Zeigefinger an deine Schläfe.\n"
                            "Du kannst sogar durch die Maske Jules hochgezogene Augenbraue sehen, während sie den Kopf schüttelt und dann beginnt voranzuschwimmen.\n Du folgst ihr und tatsächlich erkennst du einen dunklen Schatten einige Meter entfernt von euch.\n"
                            "Ihr entschließt euch näher zu schwimmen und werdet belohnt. Ein Walhai gleitet über euch hinweg und saugt eine große Menge Plankton ein.\n Ihr beobachtet eine gefühlte Ewigkeit, wie der Meeresriese durch das Wasser gleitet.\n"
                            "Dann reißt dich ein Schwall Blasen aus deiner Trance und eigenartigerweise hörst du Jules schmunzelnde Stimme: Schade dass es nur ein Traum ist oder?\n",wait_after= True)
            self.print_text("Du schaust dich irritiert zu ihr um und .... erwachst.\n",wait_after= True)
            self.epilog_path = "Special_Walhai"
            self.fadeout_music(3000)
            self.prompt_save_game()
            self.chapter1()
        else:
            self.print_text("Misserfolg! Bleibst in deiner Sphäre",wait_after= True)
            self.print_text(
                "Jule ist sichtlich nicht sehr begeistert darüber, dass du dich nicht von Ort und Stelle bewegst, \n entschließt sich aber, dich nicht allein zu lassen und schwimmt zu dir herüber.\n")
            self.print_text(
                "Als sie die Sphäre erreicht, kannst du ihre schmunzelnde Stimme in deinem Kopf hören: Du bist so ein Vollpfosten.\n ",wait_after= True)
            self.print_text("Du musst lachen und .... wachst auf.\n",wait_after= True)
            self.epilog_path = "Special_Vollpfosten"
            self.prompt_save_game()
            self.fadeout_music(3000)
            self.chapter1()

    def dich_orientieren(self):
        self.print_text("Du orientierst dich und hast zunächst wirklich nicht die leiseste Ahnung, wo du bist.\n",wait_after= True)
        wurf, zielwert = self.roll_d20_mod("Intelligenz")
        self.print_text(f"Du würfelst eine {wurf}.",wait_after= True)
        if wurf >= zielwert:
            self.navigieren()
        else:
            self.print_text(
                "Misserfolg! Navigation ist nicht so deine Stärke was? Nach einer Weile entschließt du dich langsam aufzutauchen und sobald du die Wasseroberfläche durchbrochen hast,\n "
                "wachst du auf.\n",wait_after= True)
            self.epilog_path = "orientieren_fail"
            self.prompt_save_game()
            self.fadeout_music(3000)
            self.chapter1()

    def navigieren(self):
        self.print_text(
            "Erfolg! Du weißt zwar nicht wo du bist, aber deine Sinne beginnen sich zu schärfen und du beginnst zu lauschen.\n Und tatsächlich, du hörst ein charakteristisches Brummen von Tönen… .\n",wait_after= True)
        self.fade_music_to_volume(0.1, duration=3)
        self.play_sound("Morse.mp3", volume=2.0)
        choice = self.slow_input(
            "Weißt du was die Nachricht bedeutet? \n1: Na klar, bin ja nicht von gestern. \n2: Nein, ich brauche einen Telefonjoker.\n ").lower()
        if choice == "1":
            self.fadeout_sound(3000)
            self.fade_music_to_volume(1, duration=3)
            self.play_music("ÓlafurArnalds.mp3")
            correct_sequence: List[Tuple[Literal['n', 'w', 'o'], int]] = [
                ("n", 20), ("w", 25), ("n", 20), ("o", 24),
                ("n", 100), ("w", 50), ("n", 20), ("o", 5)
            ]
            input_sequence: List[Tuple[Literal['n', 'w', 'o'], int]] = []
            direction_descriptions = {
                "n": [
                    f"Du schwimmst nach Norden durch eine dichte Seegraswiese.\n",
                    f"Du tauchst in nördlicher Richtung zwischen hoch aufragenden Korallenbänken hindurch.\n",
                    f"Nach Norden schwimmend, findest du eine Gruppe neugieriger Fische.\n"
                ],
                "w": [
                    f"Du schwimmst nach Westen entlang eines Korallenriffs.\n",
                    f"Im Westen durchquerst du ein Feld farbenfroher Anemonen.\n",
                    f"Nach Westen gleitest du an einem versunkenen Schiffswrack vorbei.\n"
                ],
                "o": [
                    f"Du schwimmst nach Osten durch klares, Blauwasser.\n",
                    f"Im Osten siehst du eine geheimnisvolle Höhle in der Ferne.\n",
                    f"Du tauchst  nach Osten und entdeckst einen alten, verrosteten Anker.\n"
                ]
            }

            for direction, distance in correct_sequence:
                dir_input = self.slow_input("In welche Richtung geht es? \n").strip().lower()
                dist_input = self.slow_input("Wie viele Meter?\n").strip()
                try:
                    dist_input = int(dist_input)
                except ValueError:
                    self.print_text("Ungültige Eingabe. Bitte versuche es erneut.\n")
                    break  # Falls eine Eingabe ungültig ist, zum Anfang der Schleife zurückkehren

                try:
                    dir_literal = self.get_literal_direction(dir_input)
                except ValueError:
                    self.print_text("Ungültige Richtung. Bitte versuche es erneut.\n")
                    break

                input_sequence.append((dir_literal, dist_input))

                if dir_literal in direction_descriptions:
                    description = random.choice(direction_descriptions[dir_literal])
                    self.print_text(description)

            if input_sequence == correct_sequence:
                self.print_text(
                    "Du bist dir sehr sicher, dass du den Anweisungen genau gefolgt bist und schaust dich am Zielort um \nund du findest tatsächlich eine klischeehafte Holzkiste. Du hast einen Schatz gefunden!\n",wait_after= True)
                self.looten()
            else:
                self.print_text("Falsche Eingabe. Du musst zum Anfang der Sequenz zurückkehren.\n",wait_after= True)
        elif choice == "2":
            self.print_text("Du hörst weiter zu...")

    def looten(self):
        self.print_text(
            "Du schaust nochmal auf deine Tauchuhr, siehst deinen Schwimmverlauf und fühlst dich ein wenig verarscht,\n aber dass du eine Schatzkiste gefunden hast, macht den kurz aufkommenden Ärger wieder wett.\n",wait_after= True)
        self.print_text(
            "Beinahe zu deiner Enttäuschung siehst du dass die Schatzkiste nicht mit einem Schloss verschlossen ist \nund öffnest sie. Du findest in der Schatzkiste eine grüne Brille, ein Tagebuch und einen Griff.\n",wait_after= True)
        self.print_text(
            "Dein Inventar wurde um >> Der widerhallende Griff << >>Die Brille des smaragdgrünen Blicks<< und das  >>Buch der Mythen<< erweitert\n",wait_after= True)
        self.print_text(
            "Alles kommt dir bekannt vor, was machen diese Gegenstände in der Kiste? Du nimmst dir das Buch \nund als du hindurch blätterst scheint alles so wie immer, aber eine Seite ganz am Ende zeigt dir etwas neues:\n Du schaust hin und liest: \nWach auf!",wait_after= True)
        self.print_text("Und du wachst auf.\n",wait_after= True)
        self.epilog_path = "Orientieren_success"
        self.prompt_save_game()
        self.fadeout_music(3000)
        self.chapter1()

    def chapter1(self):
        self.play_music("theory.mp3")
        self.print_text("Du erwachst in deinem Bett.\n")
        self.print_text("........................................................................................\n"
                        "..............................Hier entsteht Chapter1....................................\n"
                        "...................................Deine Reise..........................................\n"
                        "........................................................................................\n"
                        "Wenn dir eine Kristallkugel die Wahrheit über Dich, Dein Leben, Deine Zukunft und alles andere\n "
                        "verraten könnte, was würdest du wissen wollen?...............................................\n"
                        "Danke, fürs Zocken!\n"
                        "Entwickler: Jule\n"
                        "Skript: Auch Jule\n"
                        "Design: Immer noch Jule\n"
                        "Musik: :D \n"
                        "Entwickelt für Boje und seinem Eintritt in die epischen Dreißiger gewidmet ;)\n",wait_after= True)
        self.display_ascii("Abspann.txt")
        ####if self.epilog_path == "schoener_traum":
        ###    self.print_text("Nach deinem erholsamen Traum wachst du entspannt auf und streckst dich.")
        ###    self.print_text("Der Wecker zeigt 06:30 Uhr an und du fühlst dich bereit für den Tag.")
        ###elif self.epilog_path == "alptraum":
        ###    self.print_text("Schweißgebadet wachst du aus einem Albtraum auf. Dein Herz rast und du kannst dich kaum beruhigen.")
        ###    self.print_text("Der Wecker zeigt 06:30 Uhr an und du fühlst dich erschöpft.")
        self.print_text(f"Ergebnisse: {self.results}")


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
        game.print_text("Wähle drei Eigenschaften, von denen du denkst, dass sie am wichtigsten für dich sind:\n")
        available_attributes = list(self.attributes.keys())
        selected = 0
        game.print_text("Verfügbare Eigenschaften:\n")
        for attribute in available_attributes:
            game.print_text(f"- {attribute}\n")
        while selected < 3:
            choice = game.slow_input(f"Wähle Eigenschaft {selected + 1}: ").strip()
            if choice in self.selected_attributes:
                game.print_text("Das hast du schon ausgewählt, wähle etwas anderes.\n")
            elif choice in available_attributes:
                self.selected_attributes[choice] = self.attributes[
                                                       choice] + 7  # Bonus von 2 auf die ausgewählten Eigenschaften
                available_attributes.remove(choice)
                selected += 1
            else:
                game.print_text("Ungültige Auswahl. Bitte wähle eine gültige Eigenschaft.\n")

        for attribute in self.selected_attributes:
            self.attributes[attribute] = self.selected_attributes[attribute]

        game.print_text(
            "Ob das so eine gute Auswahl war? Wir werden ja sehen wohin das führt. Ich fasse nochmal zusammen:\n")
        for attribute, value in self.selected_attributes.items():
            game.print_text(f"{attribute}: {value}\n")

    def __str__(self):
        return (f"{self.name}'s Attributes:\n" +
                "\n".join([f"{attr}: {value}" for attr, value in self.attributes.items()]))


def main():
    global game
    game = Game()
    game.start_new_game()

    while True:
        if not game.main_event_queue.empty():
            event = game.main_event_queue.get()
            if isinstance(event, tuple) and event[0] == 'render':
                game.render_text_to_screen(event[1])

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
