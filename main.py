"""
Language learning game module with multiple difficulty levels and language support.
Handles game logic, scoring, and highscore management.
"""
import os
import random
import json


def load_highscore_data():
    """
    Load highscore data from a JSON file.
    :return:
    """
    if os.path.exists('highscore.json'):
        if os.path.getsize('highscore.json') > 0:
            with open('highscore.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return {}  # returns empty dict if highscore is empty
    else:
        return {}


def save_highscore(highscore):
    """
    Save highscore data to a JSON file.
    :param highscore:
    :return:
    """
    with open('highscore.json', 'w', encoding='utf-8') as file:
        json.dump(highscore, file, indent=4)


def reset_highscores(interface_language):
    """
    Reset highscores by clearing the JSON file.
    :param interface_language:
    :return:
    """
    translations = {
        "en": "Highscores have been reset.",
        "fr": "Les meilleurs scores ont été réinitialisés.",
        "de": "Die Highscores wurden zurückgesetzt."
    }
    with open('highscore.json', 'w', encoding='utf-8') as file:
        json.dump({}, file, indent=4)
    print(translations[interface_language] + "\n")


def language_chooser():
    """
    Choose the interface language.
    :return:
    """
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
    """
    Choose the language to learn.
    :param lang:
    :return:
    """
    while True:
        if lang == 'en':
            print("Choose a language to learn:")
            print("1. French")
            print("2. German")
            choice = input("Enter 1 or 2: \n")
            if choice == '1':
                print("\n")
                return 'fr'
            elif choice == '2':
                print("\n")
                return 'de'
        elif lang == 'fr':
            print("Choisissez une langue à apprendre:")
            print("1. Anglais")
            print("2. Allemand")
            choice = input("Entrez 1 ou 2: \n")
            if choice == '1':
                print("\n")
                return 'en'
            elif choice == '2':
                print("\n")
                return 'de'
        elif lang == 'de':
            print("Wähle eine Sprache zum Lernen:")
            print("1. Englisch")
            print("2. Französisch")
            choice = input("Geben Sie 1 oder 2 ein: \n")
            if choice == '1':
                print("\n")
                return 'en'
            elif choice == '2':
                print("\n")
                return 'fr'
        else:
            print("Invalid language. Exiting.\n")
            return None

        print("Invalid choice. Please enter 1 or 2.\n")


def gamemode_chooser(lang):
    """
    Choose the game mode.
    :param lang:
    :return:
    """
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


def play_game(language, difficulty, interface_language):
    """
    Main game logic.
    :param language:
    :param difficulty:
    :param interface_language:
    :return:
    """
    # Translations for messages
    translations = {
        "en": {
            "correct": "Correct!",
            "incorrect": "Incorrect. Try again.",
            "options": "Options",
            "your_answer": "Your answer",
            "game_over": "Game over! Your total score is",
            "new_highscore": "New high score! Previous",
            "highscore_remains": "High score remains",
            "correct_answer": "The correct answer was"
        },
        "fr": {
            "correct": "Correct!",
            "incorrect": "Incorrect. Réessayez.",
            "options": "Options",
            "your_answer": "Votre réponse",
            "game_over": "Jeu terminé! Votre score total est",
            "new_highscore": "Nouveau meilleur score! Précédent",
            "highscore_remains": "Le meilleur score reste",
            "correct_answer": "La bonne réponse était"
        },
        "de": {
            "correct": "Richtig!",
            "incorrect": "Falsch. Versuchen Sie es erneut.",
            "options": "Optionen",
            "your_answer": "Ihre Antwort",
            "game_over": "Spiel vorbei! Ihre Gesamtpunktzahl ist",
            "new_highscore": "Neuer Highscore! Vorher",
            "highscore_remains": "Highscore bleibt",
            "correct_answer": "Die richtige Antwort war"
        }
    }

    # Load the JSON data from words.json
    with open('words.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    if language not in data:
        print("Language not supported.")
        return

    t = translations[interface_language]
    questions = data[language]
    random.shuffle(questions)  # random questions
    total_score = 0

    for question in questions:
        print("\n" + question["sentence"])
        attempts = 0
        points = 2  # Start with 2 points for the first attempt

        if difficulty == "easy":
            options = question["easy_options"]
        elif difficulty == "medium":
            options = question["medium_options"]
        else:  # Hard mode
            options = []

        while attempts < 3:
            if options:
                print(f"{t['options']}: {', '.join(options)}")

            guess = input(f"{t['your_answer']}: ").strip()
            if guess.lower() == question["answer"].lower():
                print(t["correct"])
                total_score += points
                break
            else:
                attempts += 1
                points = max(0, points - 1)  # Reduce points for wrong answer
                if attempts < 3:  # Only show retry message if attempts remain
                    print(t["incorrect"])

        if attempts == 3:
            print(f"{t['correct_answer']}: {question['answer']}")

    print(f"\n{t['game_over']}: {total_score}")

    highscores = load_highscore_data()
    if language not in highscores:
        highscores[language] = 0

    if total_score > highscores[language]:
        print(f"{t['new_highscore']}: {highscores[language]}, {total_score}")
        highscores[language] = total_score
        save_highscore(highscores)
    else:
        print(f"{t['highscore_remains']}: {highscores[language]}")


def main():
    """
    Main function to run the game.
    :return:
    """
    translations = {
        "en": {
            "interface_language": "Interface Language",
            "language_to_learn": "Language to Learn",
            "difficulty": "Difficulty",
            "game_start": "Starting the game...",
            "reset_highscores": "Do you want to reset all highscores? (yes/no)"
        },
        "fr": {
            "interface_language": "Langue de l'interface",
            "language_to_learn": "Langue à apprendre",
            "difficulty": "Difficulté",
            "game_start": "Démarrage du jeu...",
            "reset_highscores": "Voulez-vous réinitialiser tous les meilleurs scores ? (oui/non)"
        },
        "de": {
            "interface_language": "gewählte Sprache",
            "language_to_learn": "Sprache zum Lernen",
            "difficulty": "Schwierigkeit",
            "game_start": "Spiel wird gestartet...",
            "reset_highscores": "Möchten Sie alle Highscores zurücksetzen? (ja/nein)"
        }
    }

    interface_language = language_chooser()
    t = translations[interface_language]

    # Ask if the user wants to reset highscores
    reset_choice = input(f"{t['reset_highscores']}: ").strip().lower()
    if reset_choice in ['yes', 'oui', 'ja', 'y', 'o', 'j']:
        reset_highscores(interface_language)

    language_to_learn = language_to_learn_chooser(interface_language)
    if not language_to_learn:
        print("Invalid language choice. Exiting.")
        return
    difficulty_choice = gamemode_chooser(interface_language)

    # Map difficulty choice to difficulty level
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
    difficulty = difficulty_map.get(difficulty_choice, 'hard')

    print(f"{t['interface_language']}: {interface_language}")
    print(f"{t['language_to_learn']}: {language_to_learn}")
    print(f"{t['difficulty']}: {difficulty}\n")
    print(t["game_start"])

    # Start the game
    play_game(language_to_learn, difficulty, interface_language)


if __name__ == "__main__":
    main()
