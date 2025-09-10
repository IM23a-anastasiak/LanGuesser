import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

HIGHSCORE_FILE = "highscore.json"
WORDS_FILE = "words.json"

TRANSLATIONS = {
    "en": {
        "app_title": "LanGuesser",
        "interface_language": "Interface Language",
        "language_to_learn": "Language to Learn",
        "difficulty": "Difficulty",
        "start_game": "Start Game",
        "reset_highscores": "Reset Highscores",
        "game_start": "Starting the game...",
        "correct": "Correct!",
        "incorrect": "Incorrect. Try again.",
        "options": "Options",
        "your_answer": "Your answer",
        "game_over": "Game over! Your total score is",
        "new_highscore": "New high score! Previous",
        "highscore_remains": "High score remains",
        "correct_answer": "The correct answer was",
        "choose_words": "Could not find words.json. Please select it.",
        "reset_done": "Highscores have been reset.",
        "send": "Send",
        "select_words": "Select words.json",
        "no_data_for_lang": "Language not supported in words.json.",
        "not_in_game": "Click 'Start Game' to begin.",
    },
    "fr": {
        "app_title": "LanGuesser",
        "interface_language": "Langue de l'interface",
        "language_to_learn": "Langue à apprendre",
        "difficulty": "Difficulté",
        "start_game": "Démarrer",
        "reset_highscores": "Réinitialiser les meilleurs scores",
        "game_start": "Démarrage du jeu...",
        "correct": "Correct !",
        "incorrect": "Incorrect. Réessayez.",
        "options": "Options",
        "your_answer": "Votre réponse",
        "game_over": "Jeu terminé ! Votre score total est",
        "new_highscore": "Nouveau meilleur score ! Précédent",
        "highscore_remains": "Le meilleur score reste",
        "correct_answer": "La bonne réponse était",
        "choose_words": "Impossible de trouver words.json. Veuillez le sélectionner.",
        "reset_done": "Les meilleurs scores ont été réinitialisés.",
        "send": "Envoyer",
        "select_words": "Sélectionnez words.json",
        "no_data_for_lang": "Langue non prise en charge dans words.json.",
        "not_in_game": "Cliquez sur « Démarrer » pour commencer.",
    },
    "de": {
        "app_title": "LanGuesser",
        "interface_language": "gewählte Sprache",
        "language_to_learn": "Sprache zum Lernen",
        "difficulty": "Schwierigkeit",
        "start_game": "Spiel starten",
        "reset_highscores": "Highscores zurücksetzen",
        "game_start": "Spiel wird gestartet...",
        "correct": "Richtig!",
        "incorrect": "Falsch. Versuchen Sie es erneut.",
        "options": "Optionen",
        "your_answer": "Ihre Antwort",
        "game_over": "Spiel vorbei! Ihre Gesamtpunktzahl ist",
        "new_highscore": "Neuer Highscore! Vorher",
        "highscore_remains": "Highscore bleibt",
        "correct_answer": "Die richtige Antwort war",
        "choose_words": "words.json nicht gefunden. Bitte wählen.",
        "reset_done": "Die Highscores wurden zurückgesetzt.",
        "send": "Senden",
        "select_words": "words.json auswählen",
        "no_data_for_lang": "Sprache wird in words.json nicht unterstützt.",
        "not_in_game": "Klicken Sie auf „Spiel starten“, um zu beginnen.",
    },
}

LANG_TO_LEARN_BY_UI = {"en": ["fr", "de"], "fr": ["en", "de"], "de": ["en", "fr"]}
DIFF_LABELS = {"en": ["Easy", "Medium", "Hard"],
               "fr": ["Facile", "Moyen", "Difficile"],
               "de": ["Einfach", "Mittel", "Schwer"]}

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE) and os.path.getsize(HIGHSCORE_FILE) > 0:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_highscore(data):
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def reset_highscores():
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=4, ensure_ascii=False)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("960x540")
        self.title("Language Trainer")
        self.configure(bg="#0e1013")
        self.resizable(False, False)

        # state
        self.interface_lang = tk.StringVar(value="en")
        self.learn_lang = tk.StringVar(value="fr")
        self.diff_label = tk.StringVar(value="Easy")
        self.input_var = tk.StringVar()

        self.words_path = WORDS_FILE if os.path.exists(WORDS_FILE) else None
        self.questions = []
        self.q_idx = -1
        self.attempts = 0
        self.points_for_q = 2
        self.total_score = 0
        self.in_game = False

        # canvas UI
        self.canvas = tk.Canvas(self, bg="#181b20", width=960, height=540,
                                bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # layout rectangles (visual sections)
        # left sidebar
        self.canvas.create_rectangle(0, 0, 300, 540, fill="#13161a", outline="")
        # top bar on right
        self.canvas.create_rectangle(316, 16, 944, 64, outline="#3a3f46")
        # question area
        self.canvas.create_rectangle(316, 80, 944, 300, outline="#3a3f46")
        # input/send area
        self.canvas.create_rectangle(316, 312, 944, 360, outline="#3a3f46")
        # log area
        self.canvas.create_rectangle(316, 376, 944, 520, outline="#3a3f46")
        # accent strip
        self.canvas.create_rectangle(0, 536, 960, 540, fill="#23e340", outline="")

        # --- widgets on canvas (create_window) ---
        # titles/labels
        self.title_lbl = ttk.Label(self, text="Language Trainer", font=("Segoe UI", 16, "bold"))
        self.canvas.create_window(16, 16, anchor="nw", window=self.title_lbl)

        # Interface language
        self.if_lang_lbl = ttk.Label(self, text="Interface Language")
        self.canvas.create_window(16, 60, anchor="nw", window=self.if_lang_lbl)
        self.if_lang_combo = ttk.Combobox(self, textvariable=self.interface_lang, values=["en", "fr", "de"], state="readonly", width=10)
        self.canvas.create_window(16, 86, anchor="nw", window=self.if_lang_combo)

        # Language to learn
        self.learn_lbl = ttk.Label(self, text="Language to Learn")
        self.canvas.create_window(16, 126, anchor="nw", window=self.learn_lbl)
        self.learn_combo = ttk.Combobox(self, textvariable=self.learn_lang,
                                        values=LANG_TO_LEARN_BY_UI[self.interface_lang.get()],
                                        state="readonly", width=10)
        self.canvas.create_window(16, 152, anchor="nw", window=self.learn_combo)

        # Difficulty
        self.diff_lbl = ttk.Label(self, text="Difficulty")
        self.canvas.create_window(16, 192, anchor="nw", window=self.diff_lbl)
        self.diff_combo = ttk.Combobox(self, textvariable=self.diff_label,
                                       values=DIFF_LABELS[self.interface_lang.get()],
                                       state="readonly", width=12)
        self.canvas.create_window(16, 218, anchor="nw", window=self.diff_combo)

        # Buttons
        self.start_btn = ttk.Button(self, text="Start Game", command=self.start_game)
        self.canvas.create_window(16, 266, anchor="nw", window=self.start_btn, width=128, height=32)
        self.reset_btn = ttk.Button(self, text="Reset Highscores", command=self.on_reset)
        self.canvas.create_window(156, 266, anchor="nw", window=self.reset_btn, width=128, height=32)

        # Words selector if missing
        self.words_btn = ttk.Button(self, text="Select words.json", command=self.choose_words)
        if not self.words_path:
            self.canvas.create_window(16, 314, anchor="nw", window=self.words_btn, width=268, height=30)

        # Top bar on right: (optional small selector caption)
        self.top_caption = ttk.Label(self, text="Vocab Practice", font=("Segoe UI", 11))
        self.canvas.create_window(328, 26, anchor="nw", window=self.top_caption)

        # Question + options
        self.sentence_var = tk.StringVar(value="")
        self.sentence_lbl = ttk.Label(self, textvariable=self.sentence_var, font=("Segoe UI", 13))
        self.canvas.create_window(328, 92, anchor="nw", window=self.sentence_lbl, width=600)

        self.options_var = tk.StringVar(value="")
        self.options_lbl = ttk.Label(self, textvariable=self.options_var)
        self.canvas.create_window(328, 136, anchor="nw", window=self.options_lbl, width=600)

        # Input + send
        self.input_entry = ttk.Entry(self, textvariable=self.input_var)
        self.canvas.create_window(328, 324, anchor="nw", window=self.input_entry, width=520, height=26)
        self.send_btn = ttk.Button(self, text="Send", command=self.on_send)
        self.canvas.create_window(860, 320, anchor="nw", window=self.send_btn, width=72, height=32)

        # Log panel
        self.log = tk.Text(self, wrap="word", state="disabled", bg="#1b1f25", fg="#e8e8e8",
                           relief="flat")
        self.canvas.create_window(328, 388, anchor="nw", window=self.log, width=600, height=120)

        # style tweaks (ttk default theme can be bland)
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except:
            pass
        style.configure("TLabel", background="#0e1013", foreground="#e8e8e8")
        style.configure("TButton", padding=6)
        style.configure("TCombobox", fieldbackground="#232831", background="#232831", foreground="#e8e8e8")

        # events
        self.bind("<Return>", lambda e: self.on_send())
        self.if_lang_combo.bind("<<ComboboxSelected>>", lambda e: self.on_interface_change())

        # initial i18n
        self.refresh_labels()

        # disable send until game starts
        self.set_send_enabled(False)

    # --- helpers ---
    def t(self, key):
        lang = self.interface_lang.get()
        return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

    def refresh_labels(self):
        self.title(self.t("app_title"))
        self.title_lbl.config(text=self.t("app_title"))
        self.if_lang_lbl.config(text=self.t("interface_language"))
        self.learn_lbl.config(text=self.t("language_to_learn"))
        self.diff_lbl.config(text=self.t("difficulty"))
        self.start_btn.config(text=self.t("start_game"))
        self.reset_btn.config(text=self.t("reset_highscores"))
        self.send_btn.config(text=self.t("send"))
        if not self.words_path:
            self.words_btn.config(text=self.t("select_words"))
        # update combos according to UI language
        self.learn_combo["values"] = LANG_TO_LEARN_BY_UI[self.interface_lang.get()]
        if self.learn_lang.get() not in self.learn_combo["values"]:
            self.learn_lang.set(self.learn_combo["values"][0])
        labels = DIFF_LABELS[self.interface_lang.get()]
        if self.diff_label.get() not in labels:
            self.diff_label.set(labels[0])
        self.diff_combo["values"] = labels

    def on_interface_change(self):
        self.refresh_labels()

    def choose_words(self):
        path = filedialog.askopenfilename(
            title=self.t("select_words"),
            filetypes=[("JSON", "*.json"), ("All files", "*.*")]
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    json.load(f)
                self.words_path = path
                # hide the button (move off-canvas by deleting its window and rectangle not needed)
                self.canvas.delete(self.words_btn)  # harmless if not present
                self.words_btn.place_forget() if hasattr(self.words_btn, "place_info") else None
            except Exception as e:
                messagebox.showerror(self.t("select_words"), str(e))

    def log_write(self, text):
        self.log.config(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def diff_internal(self):
        lbl = self.diff_label.get()
        for lang, labels in DIFF_LABELS.items():
            if lbl in labels:
                idx = labels.index(lbl)
                return ["easy", "medium", "hard"][idx]
        return "hard"

    # --- game flow ---
    def start_game(self):
        if not self.words_path or not os.path.exists(self.words_path):
            messagebox.showwarning(self.t("app_title"), self.t("choose_words"))
            self.choose_words()
            if not self.words_path:
                return
        try:
            with open(self.words_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror(self.t("app_title"), str(e))
            return

        target_lang = self.learn_lang.get()
        if target_lang not in data:
            messagebox.showerror(self.t("app_title"), self.t("no_data_for_lang"))
            return

        self.questions = data[target_lang]
        self.q_idx = -1
        self.attempts = 0
        self.points_for_q = 2
        self.total_score = 0
        self.in_game = True
        self.set_send_enabled(True)
        self.input_var.set("")
        self.input_entry.focus_set()
        self.log_write(self.t("game_start"))
        self.next_question()

    def next_question(self):
        self.q_idx += 1
        self.attempts = 0
        self.points_for_q = 2
        if self.q_idx >= len(self.questions):
            self.finish_game()
            return
        q = self.questions[self.q_idx]
        self.sentence_var.set(q.get("sentence", ""))

        diff = self.diff_internal()
        if diff == "easy":
            opts = q.get("easy_options", [])
        elif diff == "medium":
            opts = q.get("medium_options", [])
        else:
            opts = []
        self.options_var.set(f"{self.t('options')}: {', '.join(opts)}" if opts else "")
        self.input_var.set("")

    def on_send(self):
        if not self.in_game:
            self.log_write(self.t("not_in_game"))
            return
        guess = self.input_var.get().strip()
        if not guess:
            return
        q = self.questions[self.q_idx]
        correct = q.get("answer", "").strip()

        if guess.lower() == correct.lower():
            self.log_write(self.t("correct"))
            self.total_score += self.points_for_q
            self.next_question()
        else:
            self.attempts += 1
            self.points_for_q = max(0, self.points_for_q - 1)
            if self.attempts < 3:
                self.log_write(self.t("incorrect"))
            else:
                self.log_write(f"{self.t('correct_answer')}: {correct}")
                self.next_question()

    def finish_game(self):
        self.in_game = False
        self.set_send_enabled(False)
        self.log_write(f"{self.t('game_over')}: {self.total_score}")
        hs = load_highscore()
        key = self.learn_lang.get()
        prev = hs.get(key, 0)
        if self.total_score > prev:
            self.log_write(f"{self.t('new_highscore')}: {prev}, {self.total_score}")
            hs[key] = self.total_score
            save_highscore(hs)
        else:
            self.log_write(f"{self.t('highscore_remains')}: {prev}")

    def on_reset(self):
        reset_highscores()
        self.log_write(self.t("reset_done"))

    def set_send_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.send_btn.config(state=state)
        self.input_entry.config(state=state)

if __name__ == "__main__":
    app = App()
    app.mainloop()
