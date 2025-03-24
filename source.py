import subprocess
import sys
import os


def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def ensure_packages(packages):
    for package, import_name in packages.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"{package} not found. Installing...")
            install_package(package)


required_packages = {
    "discord.py-self": "discord",
    "pyperclip": "pyperclip",
    "pyttsx3": "pyttsx3",
    "rapidfuzz": "rapidfuzz",
    "customtkinter": "customtkinter",
}

ensure_packages(required_packages)

import discord
import pyperclip
import pyttsx3
from rapidfuzz import process, fuzz
import customtkinter as ctk
import threading
import asyncio

FILE = "token.txt"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def read_token():

    if not os.path.exists(FILE):
        print("Please add your token to 'token.txt' and rerun the program.")
        with open(FILE, "w") as file:
            file.write("")
        exit(1)

    with open(FILE, "r") as file:
        token = file.read().strip()

    if not token:
        print(
            "Token file is empty. Please add your token to 'token.txt' and rerun the program."
        )
        exit(1)

    return token


# Your personal token (Keep it private!)
TOKEN = read_token()
SOURCE_CHANNEL_ID = 1348415113228718151  # Channel to copy messages from

# SERVER NAMES:
SERVER_NAME_FIRST = {
    "lunar",
    "savage",
    "blessed",
    "infernal",
    "enchanted",
    "eternal",
    "fiery",
    "ironclad",
    "crystal",
    "frozen",
    "glowing",
    "radiant",
    "cursed",
    "frostbitten",
    "blazing",
    "brutal",
    "gleaming",
    "phantom",
    "whispering",
    "silver",
    "flaming",
    "shadowy",
    "arcane",
    "shadowed",
    "stormy",
    "thunderous",
    "golden",
    "vengeful",
    "ancient",
    "wild",
    "mystic",
    "dark",
    "wicked",
    "gloomy",
    "sinister",
    "merciless",
    "twilight",
    "venomous",
}

SERVER_NAME_SECOND = {
    "crossbow",
    "glaive",
    "shield",
    "scepter",
    "axe",
    "chalice",
    "banner",
    "mace",
    "medallion",
    "tome",
    "pendant",
    "bear",
    "amulet",
    "bracelet",
    "orb",
    "blade",
    "sword",
    "staff",
    "necklace",
    "hammer",
    "armor",
    "boots",
    "relic",
    "cuirass",
    "scroll",
    "talisman",
    "lantern",
    "bow",
    "cloak",
    "gauntlets",
    "dagger",
    "tunic",
    "potion",
    "cudgel",
    "helm",
    "spear",
    "gauntlet",
    "ring",
    "quiver",
}


TREANT_KEYWORDS = {
    "treant",
    "groot",
    "tree",
    "trent",
    "elder",
    "trant",
    "edler",
    "eldar",
    "tyrant",
    "tyrant,",
    "treeant",
    "big",
    "treat",
    "man",
    "🌲",
    "🎄",
    "branch",
    "treaant",
    "eldertreant",
    "trench",
}

RUNE_GOLEM_KEYWORDS = {"rune", "golem", "rg", "rungolem", "runegolem", "rgolem"}

LICHT_KING_KEYWORDS = {"licht", "lk", "lichtking", "lichtk", "lichtkng", "lich"}

keywords = TREANT_KEYWORDS


BANNED_KEYWORDS = {
    "lf",
    "group",
    "if",
    "gc",
    "dm",
    "hopping",
    "hop",
    "serverhopping",
    "need",
    "trading",
    "looking",
    "farm",
    "farms",
}

SYMBOLS = {
    ",",
    "/",
    "\\",
    "\n",
    "|",
    "‘",
    "*",
    ")",
    "(",
    ":",
    ";",
    "!",
    "-",
    "#",
    "[",
    "]",
}

California = {"cali", "cal", "california", "cl", "ca"}
Singapore = {"sg", "singapore", "west", "nwsg", "nw", "northwest", "north-west"}
Texas = {"tx", "texas", "tex", "texts"}
Oregon = {"or", "oregon", "org", "oregan", "oregeon"}
Hesse = {"hesse", "germany", "de", "gesse"}
Unknown = {"unknown", "unkown", "unk", "unknow", "ur"}
Holland = {"holland", "netherlands", "nl", "holand"}
Florida = {"fl", "florida"}
Washington = {"wa", "washington"}
India = {"india", "maharatasha", "maharashtra", "mahatrasha"}


def speak(text, volume=0.4):
    engine = pyttsx3.init()
    engine.setProperty("volume", max(0.0, min(volume, 1.0)))
    engine.say(text)
    engine.runAndWait()


def speak_region(server_name, words, mode):
    words = set(words)

    region = ""
    location = ""

    if words & California:
        region = "California"
    elif words & Singapore:
        region = "Singapore"
    elif words & Texas:
        region = "Texas"
    elif words & Oregon:
        region = "Oregon"
    elif words & Hesse:
        region = "Hesse"
    elif words & Unknown:
        region = "Unknown"
    elif words & Holland:
        region = "Holland"
    elif words & Florida:
        region = "Florida"
    elif words & Washington:
        region = "Washington"
    elif words & India:
        region = "India"
    else:
        region = "No Region"

    if mode == "treant" or mode == "licht":
        speak(f"{server_name}, {region}")
        return

    if words & {"forest"}:
        location = "Forest"
    elif words & {"beach"}:
        location = "Beach"
    else:
        location = "No Location"

    speak(f"{server_name}, {region}, {location}")


def correct_word(word, word_list):
    match, score, index = process.extractOne(word, word_list, scorer=fuzz.ratio)
    return (match, score) if score >= 75 else (None, 0)


def find_correct_words(words):
    best_pair = (None, None)
    best_score = 0

    for i in range(len(words) - 1):
        first_word, first_score = correct_word(words[i], SERVER_NAME_FIRST)
        second_word, second_score = correct_word(words[i + 1], SERVER_NAME_SECOND)

        if first_word and second_word:
            total_score = (first_score + second_score) / 2
            if total_score > best_score:
                best_score = total_score
                best_pair = (first_word, second_word)

    if best_pair[0] and best_pair[1]:
        return f"{best_pair[0]} {best_pair[1]}"
    return None


def check_boss(text, gui, mode):
    text = text.lower()
    if text != "" and len(text) <= 500:
        gui.log(text)

        # Check for keywords
        clean_text = text
        for symbol in SYMBOLS:
            clean_text = clean_text.replace(symbol, " ")

        words = clean_text.split()
        found_keywords = keywords & set(words)
        banned = BANNED_KEYWORDS & set(words)

        if found_keywords and not banned:
            gui.log(f"Keyword(s) {found_keywords} found")
            server_name = find_correct_words(words)

            if server_name:
                pyperclip.copy(server_name)
                gui.log("Server Name: " + server_name)
                speak_region(server_name, words, mode)

        gui.log("--------------------------------------------------")


class DiscordBot(discord.Client):
    def __init__(self, gui):
        super().__init__(self_bot=True)
        self.gui = gui

    async def on_ready(self):
        self.gui.log("Logged in Successfully")
        self.gui.log("--------------------------------------------------")
        self.gui.update_status("Running")
        self.gui.start_button.configure(state="normal")
        self.gui.start_button.configure(text="Stop")

    async def on_message(self, message):

        # print(f"Message detected in channel {message.channel.id} from {message.author}: {message.content}")

        # Ignore own messages to avoid loops
        if message.author == self.user:
            return

        # Check if the message is in the source channel and has attachments
        if message.channel.id == SOURCE_CHANNEL_ID:
            check_boss(message.content, self.gui, self.gui.mode)


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Server Sniper")
        self.geometry("800x500")

        self.labels = ctk.CTkFrame(self, fg_color="transparent")
        self.labels.pack(pady=10, side="top")

        self.stat_label = ctk.CTkLabel(
            self.labels, text="Status: Stopped", font=("Arial", 16)
        )
        self.stat_label.pack(padx=10)

        self.mode_label = ctk.CTkLabel(
            self.labels, text="Mode: Treant", font=("Arial", 16)
        )
        self.mode_label.pack(padx=10)

        self.buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons.pack(pady=10, side="top")

        self.bosses = ctk.CTkFrame(self.buttons, fg_color="transparent")
        self.bosses.pack(pady=10, padx=20, side="right")

        self.start_button = ctk.CTkButton(
            self.buttons, text="Start", command=self.start_stop
        )
        self.start_button.pack(side="left", padx=10, pady=5)

        self.switch_treant_button = ctk.CTkButton(
            self.bosses,
            text="Elder Treant",
            state="disabled",
            command=self.switch_treant,
        )
        self.switch_treant_button.pack(padx=10, pady=5)

        self.switch_rune_button = ctk.CTkButton(
            self.bosses, text="Rune Golem", command=self.switch_rune
        )
        self.switch_rune_button.pack(padx=10, pady=5)

        self.switch_licht_button = ctk.CTkButton(
            self.bosses, text="Licht King", command=self.switch_licht
        )
        self.switch_licht_button.pack(padx=10, pady=5)

        self.log_box = ctk.CTkTextbox(
            self, height=200, wrap="none", font=("Segoe UI Emoji", 14)
        )
        self.log_box.pack(pady=10, fill="both", expand=True, side="bottom")

        self.bot = None
        self.bot_thread = None
        self.mode = "treant"

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.yview_moveto(1)
        self.log_box.configure(state="disabled")

    def update_status(self, status):
        self.stat_label.configure(text=f"Status: {status}")

    def run_bot(self):
        asyncio.run(self.bot.start(TOKEN))

    def start_stop(self):
        if not self.bot:
            self.bot = DiscordBot(self)
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            self.start_button.configure(state="disabled")
            self.update_status("Starting...")
        else:
            asyncio.run_coroutine_threadsafe(self.bot.close(), self.bot.loop)
            self.bot = None
            self.update_status("Stopped")
            self.log("Bot stopped")
            self.log("--------------------------------------------------")
            self.start_button.configure(text="Start")

    def switch_treant(self):
        global keywords
        if self.mode != "treant":
            self.mode = "treant"
            keywords = TREANT_KEYWORDS
            self.mode_label.configure(text="Mode: Elder Treant")
            self.switch_treant_button.configure(state="disabled")
            self.switch_rune_button.configure(state="normal")
            self.switch_licht_button.configure(state="normal")
            self.log("Switched to Elder Treant")
            self.log("--------------------------------------------------")

    def switch_rune(self):
        global keywords
        if self.mode != "rune":
            self.mode = "rune"
            keywords = RUNE_GOLEM_KEYWORDS
            self.mode_label.configure(text="Mode: Rune Golem")
            self.switch_rune_button.configure(state="disabled")
            self.switch_treant_button.configure(state="normal")
            self.switch_licht_button.configure(state="normal")
            self.log("Switched to Rune Golem")
            self.log("--------------------------------------------------")

    def switch_licht(self):
        global keywords
        if self.mode != "licht":
            self.mode = "licht"
            keywords = LICHT_KING_KEYWORDS
            self.mode_label.configure(text="Mode: Licht King")
            self.switch_licht_button.configure(state="disabled")
            self.switch_treant_button.configure(state="normal")
            self.switch_rune_button.configure(state="normal")
            self.log("Switched to Licht King")
            self.log("--------------------------------------------------")


app = GUI()
app.mainloop()
