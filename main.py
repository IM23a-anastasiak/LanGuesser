import json


def language_chooser():
    while True:
        print("Choose a language / Choisissez une langue / Wähle eine Sprache:")
        print("1. English")
        print("2. Français")
        print("3. Deutsch")
        choice = input(f"Enter 1, 2 or 3: / Gebe 1, 2 oder 3 ein: / Entrez 1, 2 ou 3: \n")
        if choice == '1':
            print("\n")
            return 'en'
        elif choice == '2':
            print("\n")
            return 'fr'
        elif choice == '3':
            print("\n")
            return 'de'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")


def language_to_learn_chooser(lang):
    while True:
        if lang == 'en':
            print("Choose a language to learn:")
            print("1. French")
            print("2. German")
            choice = input("Enter 1 or 2: \n")
        elif lang == 'fr':
            print("Choisissez une langue à apprendre:")
            print("1. Anglais")
            print("2. Allemand")
            choice = input("Entrez 1 ou 2: \n")
        elif lang == 'de':
            print("Wähle eine Sprache zum Lernen:")
            print("1. Englisch")
            print("2. Französisch")
            choice = input(f"Geben Sie 1 oder 2 ein: \n")
        else:
            print("Invalid language. Exiting.\n")
            return None

        if choice == '1':
            print("\n")
            return 'fr' if lang == 'en' else 'en'
        elif choice == '2':
            print("\n")
            return 'de' if lang == 'en' else 'fr'
        else:
            print("Invalid choice. Please enter 1 or 2.\n")


def gamemode_chooser(lang):
    while True:
        if lang == 'en':
            print("Choose a game mode:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            choice = input("Enter 1, 2 or 3: \n")
        elif lang == 'fr':
            print("Choisissez un mode de jeu:")
            print("1. Facile")
            print("2. Moyen")
            print("3. Difficile")
            choice = input("Entrez 1, 2 ou 3: \n")
        elif lang == 'de':
            print("Wähle einen Spielmodus:")
            print("1. Einfach")
            print("2. Mittel")
            print("3. Schwer")
            choice = input("Geben Sie 1, 2 oder 3 ein: \n")
        else:
            print("Invalid language. Exiting.\n")
            return None

        if choice in ['1', '2', '3']:
            print("\n")
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")


import json


def play_game(language, difficulty):
    # Loads the JSON data from words.json
    with open('words.json', 'r') as file:
        data = json.load(file)

    if language not in data:
        print("Language not supported.")
        return

    questions = data[language]
    total_score = 0

    for question in questions:
        print("\n" + question["sentence"])
        attempts = 0
        points = 2  # Starts with 2 points for the first attempt

        if difficulty == "easy":  # easy mode
            options = question["easy_options"]
        elif difficulty == "medium":  # medium mode
            options = question["medium_options"]
        else:  # Hard mode
            options = []

        while attempts < 3:
            if options:
                print("Options:", ", ".join(options))

            guess = input("Your answer: ").strip()
            if guess.lower() == question["answer"].lower():
                print("Correct!")
                total_score += points
                break
            else:
                print("Incorrect. Try again.")
                attempts += 1
                points = max(0, points - 1)  # Reduces points for wrong answer

        if attempts == 3:
            print(f"The correct answer was: {question['answer']}")

    print(f"\nGame over! Your total score is: {total_score}")


def main():
    translations = {
        "en": {
            "interface_language": "Interface Language",
            "language_to_learn": "Language to Learn",
            "difficulty": "Difficulty",
            "game_start": "Starting the game..."
        },
        "fr": {
            "interface_language": "Langue de l'interface",
            "language_to_learn": "Langue à apprendre",
            "difficulty": "Difficulté",
            "game_start": "Démarrage du jeu..."
        },
        "de": {
            "interface_language": "gewählte Sprache",
            "language_to_learn": "Sprache zum Lernen",
            "difficulty": "Schwierigkeit",
            "game_start": "Spiel wird gestartet..."
        }
    }

    interface_language = language_chooser()
    language_to_learn = language_to_learn_chooser(interface_language)
    if not language_to_learn:
        print("Invalid language choice. Exiting.")
        return
    difficulty = gamemode_chooser(interface_language)

    # get right translation for summary
    t = translations[interface_language]
    print(f"{t['interface_language']}: {interface_language}")
    print(f"{t['language_to_learn']}: {language_to_learn}")
    print(f"{t['difficulty']}: {difficulty}\n")
    print(t["game_start"])

    # Start the game
    play_game(language_to_learn, difficulty)

if __name__ == "__main__":
    main()
