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

def main():
    interface_language = language_chooser()
    language_to_learn = language_to_learn_chooser(interface_language)
    if not language_to_learn:
        print("Invalid language choice. Exiting.")
        return
    difficulty = gamemode_chooser(interface_language)
    print(f"Interface Language: {interface_language}")
    print(f"Language to Learn: {language_to_learn}")
    print(f"Difficulty: {difficulty}")

if __name__ == "__main__":
    main()