class Character:
    def __init__(self, name, courage, wisdom, intuition, charisma, dexterity, agility, constitution, strength):
        self.name = name
        self.courage = courage
        self.wisdom = wisdom
        self.intuition = intuition
        self.charisma = charisma
        self.dexterity = dexterity
        self.agility = agility
        self.constitution = constitution
        self.strength = strength

    def __str__(self):
        return (f"Name: {self.name}, Courage: {self.courage}, Wisdom: {self.wisdom}, Intuition: {self.intuition}, "
                f"Charisma: {self.charisma}, Dexterity: {self.dexterity}, Agility: {self.agility}, "
                f"Constitution: {self.constitution}, Strength: {self.strength}")

class Companion(Character):
    def __init__(self, name, courage, wisdom, intuition, charisma, dexterity, agility, constitution, strength):
        super().__init__(name, courage, wisdom, intuition, charisma, dexterity, agility, constitution, strength)

class User(Companion):
    def __init__(self, name, courage, wisdom, intuition, charisma, dexterity, agility, constitution, strength):
        super().__init__(name, courage, wisdom, intuition, charisma, dexterity, agility, constitution, strength)

class Item:
    def __init__(self, name, description, attributes, special_ability=None):
        self.name = name
        self.description = description
        self.attributes = attributes
        self.special_ability = special_ability

    def __str__(self):
        return (f"Item: {self.name}, Description: {self.description}, Attributes: {self.attributes}, "
                f"Special Ability: {self.special_ability}")

class Quest:
    def __init__(self, name, description, questline, mode):
        self.name = name
        self.description = description
        self.questline = questline
        self.mode = mode

    def __str__(self):
        return (f"Quest: {self.name}, Description: {self.description}, Questline: {self.questline}, Mode: {self.mode}")

class Questline:
    def __init__(self, name, description, quests):
        self.name = name
        self.description = description
        self.quests = quests

    def __str__(self):
        return (f"Questline: {self.name}, Description: {self.description}, Quests: {[quest.name for quest in self.quests]}")

class Game:
    def __init__(self):
        self.companions = []
        self.users = []
        self.items = []
        self.quests = []
        self.questlines = []

    def add_companion(self, companion):
        self.companions.append(companion)

    def add_user(self, user):
        self.users.append(user)

    def add_item(self, item):
        self.items.append(item)

    def add_quest(self, quest):
        self.quests.append(quest)

    def add_questline(self, questline):
        self.questlines.append(questline)

    def travel_map(self, destination):
        print(f"Traveling to {destination}")

    def fast_travel(self, destination):
        print(f"Fast traveling to {destination}")

# Define Items
necklace_of_the_seabond = Item(
    name="Necklace of the Seabond",
    description="A precious necklace with a radiant blue aquamarine pendant.",
    attributes={"Charisma": 2, "Willpower": 2, "Intuition": 1},
    special_ability="Calm Waters: Once per day, negate fear effects and stress conditions, restoring 1D6 willpower points."
)

glasses_of_the_emerald_gaze = Item(
    name="Glasses of the Emerald Gaze",
    description="A magical pair of sunglasses protecting the wearer from harsh sunlight.",
    attributes={"Perception": 1, "Charisma": 1}
)

the_echoing_grip = Item(
    name="The Echoing Grip",
    description="An enchanted grip that amplifies the user's voice.",
    attributes={"Charisma": 1, "Leadership": 1, "Persuasion": 1},
    special_ability="Echo of Authority: Once a day, deliver a command or speech with such authority that it grants a temporary morale boost to allies within hearing range."
)

# Define Quests
relax_trust_and_let_go = Quest(
    name="Relax, Trust and Let Yourself Go",
    description="Embark on this quest after finishing the 'Soulmate Search' questline.",
    questline="Companions and Partnerships",
    mode="Mixed"
)

continuous_learning = Quest(
    name="Continuous Learning",
    description="Stay curious, pursue side quests, read, and try new things as often as your questlog allows.",
    questline="Personal Growth",
    mode="Solo"
)

work_life_balance = Quest(
    name="Work-Life Balance",
    description="Achieve the Zen Master title by harmonizing leisure and professional activities.",
    questline="Personal Growth",
    mode="Solo"
)

goals_and_dreams = Quest(
    name="Goals and Dreams",
    description="Set life goals and dreams to unlock new specific quests.",
    questline="Personal Growth",
    mode="Solo"
)

friendships_and_family = Quest(
    name="Friendships and Family",
    description="Strengthen bonds with allies and relatives by increasing quality social interaction.",
    questline="Personal Friendships and Relationships",
    mode="Mixed"
)

partnerships = Quest(
    name="Partnerships",
    description="Develop and nurture partnerships using add_companion and add_user.",
    questline="Personal Friendships and Relationships",
    mode="Mixed"
)

adventure_mode = Quest(
    name="Adventure Mode",
    description="Embark on new journeys with companions to create lasting memories.",
    questline="Adventures",
    mode="Mixed"
)

# Define Questlines
physical_attributes = Questline(
    name="Strength, Condition, Willpower and Composure: Physical Attributes",
    description="Embark on a journey to achieve peak physical condition.",
    quests=[relax_trust_and_let_go]
)

mental_attributes = Questline(
    name="Strength, Condition, Willpower and Composure: Mental Attributes",
    description="Nurture and unlock abilities to enhance Willpower, Courage, and Composure.",
    quests=[relax_trust_and_let_go]
)

personal_growth = Questline(
    name="Personal Growth Expedition",
    description="Embark on a journey of continuous learning, balancing work-life, and achieving goals.",
    quests=[continuous_learning, work_life_balance, goals_and_dreams]
)

personal_friendships = Questline(
    name="Personal Friendships and Relationships Campaign",
    description="Strengthen bonds with friends, family, and partners.",
    quests=[friendships_and_family, partnerships]
)

adventures = Questline(
    name="Adventures",
    description="Unlock adventure mode by embarking on new journeys with companions.",
    quests=[adventure_mode]
)

# Initialize the game
game = Game()

# Add Items
game.add_item(necklace_of_the_seabond)
game.add_item(glasses_of_the_emerald_gaze)
game.add_item(the_echoing_grip)

# Add Quests
game.add_quest(relax_trust_and_let_go)
game.add_quest(continuous_learning)
game.add_quest(work_life_balance)
game.add_quest(goals_and_dreams)
game.add_quest(friendships_and_family)
game.add_quest(partnerships)
game.add_quest(adventure_mode)

# Add Questlines
game.add_questline(physical_attributes)
game.add_questline(mental_attributes)
game.add_questline(personal_growth)
game.add_questline(personal_friendships)
game.add_questline(adventures)

# Example of using the new features
game.add_companion(Companion("Alice", 10, 12, 14, 13, 11, 10, 15, 14))
game.add_user(User("Bob", 11, 13, 15, 14, 12, 11, 16, 15))

print(game.companions[0])
print(game.users[0])

game.travel_map("New Zealand")
game.fast_travel("Ruhr Area")
