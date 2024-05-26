Release Information:

Der Patch v.30.0.0 wurde am 21. Mai 2024 veröffentlicht.
Neue Funktionen und Quests:

Funktionen:

Add_companion und add_user wurden implementiert, um neue Personen zu Ihrer Gruppe hinzuzufügen.
Travel_map und fast_travel wurden hinzugefügt, um neue Quests und Personen zu finden und schneller zu Zielen zu reisen.
Questline: Strength, Condition, Willpower and Composure:

Physische Attribute: Diese Questline konzentriert sich auf die Verbesserung der physischen Kondition, die eng mit den mentalen Attributen verbunden ist. Sie fördert kollaborative Aktivitäten und gemeinsame Erfahrungen.
Mentale Attribute: Diese Questline zielt darauf ab, Fähigkeiten und Techniken zu entwickeln, die Willenskraft, Mut und Gelassenheit stärken. Physische und mentale Attribute beeinflussen sich gegenseitig, und die Quests sind sowohl im Solo- als auch im Kooperationsmodus ausbalanciert.
Spezialquest:

Relax, Trust and Let Yourself Go: Diese Quest kann nach Abschluss der "Soulmate Search" Questline gestartet werden. Sie beeinflusst die physischen und mentalen Attribute des Spielers, bietet eine neue Perspektive auf das eigene Leben und verbessert das allgemeine Gameplay.
Personal Growth Expedition:

Continuous Learning: Ständiges Lernen durch Nebenquests, Lesen und das Ausprobieren neuer Dinge, um kontinuierlich neue Fähigkeiten, Wissen und Erfahrungen zu sammeln.
Work-Life Balance: Der Zen-Meister-Titel kann durch Harmonisierung von Freizeit- und Berufsaktivitäten erreicht werden.
Goals and Dreams: Das Setzen von Lebenszielen und Träumen schaltet spezifische Quests frei, die die Abenteuer vielfältig und erfüllend machen.
Personal Friendships and Relationships Campaign:

Friendships and Family: Stärkung der Beziehungen zu Verbündeten und Verwandten durch qualitativ hochwertige soziale Interaktionen. Diese Questline ist mit mentalen und physischen Attributen verwoben und kann auf Partnerschaftsquests ausgeweitet werden.
Partnerships: Partnerschaften können durch add_companion und add_user entwickelt und gepflegt werden. Diese Questline ist stark mit allen neuen Aspekten dieses Patches verbunden und kann die Gesamtkapazitäten und Zustände fördern.
Adventures:

Adventure Mode: Kann durch neue Reisen und das Mitbringen von Begleitern freigeschaltet werden. Diese Abenteuer können bleibende Erinnerungen schaffen und Questlines und Erfahrungslevel nachhaltig beeinflussen.
Neue Gegenstände und Kräfte:

Necklace of the Seabond:

Ein wertvolles Halsband mit einem leuchtend blauen Aquamarin-Anhänger, der physischen Schutz bietet und Herz und Geist stärkt.
Attribute:
Charisma +2
Willenskraft +2
Intuition +1
Spezialfähigkeit:
Calm Waters: Einmal täglich kann die beruhigende Kraft des Aquamarins genutzt werden, um Angst- und Stresszustände zu negieren und 1W6 Willenskraftpunkte wiederherzustellen.
Glasses of the Emerald Gaze:

Eine magische Sonnenbrille, die vor starkem Sonnenlicht schützt und die Coolness erhöht.
Attribute:
Verbesserte Sicht bei hellem Sonnenlicht +1 Wahrnehmung in natürlichen Umgebungen.
Charisma-Bonus: +1 Charisma bei jeder Silvesterparty.
The Echoing Grip:

Ein scheinbar gewöhnlicher Griff, der mit alter Magie verzaubert ist, um die Stimme des Benutzers zu verstärken.
Attribute:
Charisma +1
Führungsbonus +1
Überzeugung +1
Spezialfähigkeit:
Echo of Authority: Einmal am Tag kann der Benutzer den Echoing Grip aktivieren, um einen Befehl oder eine Rede mit solcher Autorität zu halten, dass es den Verbündeten in Hörweite einen vorübergehenden Moralbonus gewährt.
Bugfixes:

Companions: Begleiter, die Sie als wertvoll für Ihr Abenteuer identifizieren, können mit add_companion und add_user hinzugefügt, leicht über travel_map gefunden und über fast_travel erreicht werden. Beziehungen zu diesen Begleitern werden nicht durch Beschäftigung beeinträchtigt.
Interest Fixes: Das fehlende Interesse an Neuseeland, dem Ruhrgebiet und Eseln wurde entfernt.
Spezielle Anweisungen:

Hinweis: (Hier könnten spezielle Anweisungen oder Notizen hinzugefügt werden)
Zusammengefasst beschreibt der Patch eine Vielzahl neuer Funktionen und Quests, die auf persönliche Entwicklung, Freundschaften und Abenteuer abzielen, sowie neue Gegenstände, die das Gameplay verbessern. Fehlerbehebungen sorgen für eine reibungslosere Spielerfahrung.
Was könnte in der Readme datei stehen, sie sollte nicht nur wiedergeben, was in den Patchnotes steht

ChatGPT
Eine README-Datei sollte eine umfassendere Einführung in das Projekt geben, die über die Details eines bestimmten Patches hinausgeht. Hier ist ein Beispiel für eine README-Datei, die nicht nur die Patchnotes wiedergibt, sondern auch allgemeine Informationen über das Projekt, Installationsanweisungen, Benutzungsbeispiele und andere relevante Informationen enthält.

markdown
Copy code
# Epic 30s Quest Game

Welcome to the Epic 30s Quest Game! This game is designed to guide players through personal growth, adventures, and building relationships, all while achieving various life goals and maintaining a balance between physical and mental attributes.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [New in Patch v.30.0.0](#new-in-patch-v3000)
- [Items](#items)
- [Quests](#quests)
- [Bug Fixes](#bug-fixes)
- [Contributing](#contributing)
- [License](#license)

## Introduction
Epic 30s Quest Game is an immersive RPG that helps players navigate their 30s through a series of engaging quests, personal growth challenges, and adventures. The game integrates aspects of self-improvement, relationship building, and adventure-seeking to create a holistic and enriching gaming experience.

## Features
- Add companions and users to your party.
- Explore new quests and people using the travel map and fast travel features.
- Engage in quests that enhance both physical and mental attributes.
- Balance work-life and pursue continuous learning for personal growth.
- Strengthen friendships and family bonds, and nurture partnerships.
- Unlock adventure mode for new and exciting journeys.

## Installation
To install the game, follow these steps:

1. Clone the repository:
   git clone https://github.com/julenuy/Level_up.git
Navigate to the project directory:
  cd Level_up
Install the necessary dependencies:
  please check your birth certificate if you really turned 30. 
Copy code
pip install -r requirements.txt
Run the patch:
python epic.py

Adding Companions and Users
You can add companions and users to your party using the add_companion and add_user commands. These features help you build a supportive network as you navigate through various quests.

Traveling
Use the travel_map and fast_travel features to find new quests and people, and to travel faster to destinations. These features save time and enhance the gameplay experience.

Quests
Quests are categorized into different questlines such as physical attributes, mental attributes, personal growth, friendships and relationships, and adventures. Each questline offers unique challenges and rewards.

New in Patch v.30.0.0

Features
Add_companion and add_user: Implemented to add new people to your party.
Travel_map and fast_travel: Added to find new quests and people, and travel faster to destinations.
Questline Updates
Strength, Condition, Willpower and Composure:

Physical attributes: Achieve peak physical condition linked to mental attributes.
Mental attributes: Enhance Willpower, Courage, and Composure.
Personal Growth Expedition:

Continuous Learning: Stay curious and gain new skills.
Work-Life Balance: Achieve harmony between leisure and professional activities.
Goals and Dreams: Set and pursue life goals.
Personal Friendships and Relationships Campaign:

Friendships and Family: Strengthen bonds with allies and relatives.
Partnerships: Develop and nurture partnerships.
Adventures:

Adventure Mode: Unlock and embark on new journeys with companions.
Items

New Items and Powers
Necklace of the Seabond: Provides physical protection and strengthens the heart and mind.
Glasses of the Emerald Gaze: Protects from harsh sunlight and enhances coolness.
The Echoing Grip: Amplifies the user's voice for commanding presence and leadership.
Quests

Engage in a variety of quests designed to improve physical and mental attributes, foster personal growth, and build strong relationships.

Example Quests
Relax, Trust and Let Yourself Go: Unlocks after completing the "Soulmate Search" questline.
Continuous Learning: Encourages staying curious and gaining new skills.
Bug Fixes

Improved companion detection and interaction.
Removed missing interest to New Zealand, Ruhr Area, and Donkeys

License

This project is licensed under the NUY License. 
