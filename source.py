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
}

ensure_packages(required_packages)

import discord
import pyperclip
import pyttsx3
from rapidfuzz import process, fuzz

FILE = "token.txt"


def read_token():

    if not os.path.exists(FILE):
        print(
            "Token file is empty. Please add your token to 'token.txt' and rerun the program."
        )
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

YELLOW = "\033[93m"
RESET = "\033[0m"

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

# Set up keywords to search for
KEYWORDS = {
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
    "guy",
    "🎄",
    "branch",
    "treaant",
    "eldertreant",
}

BANNED_KEYWORDS = {
    "lf",
    "group",
    "if",
    "gc",
    "dm",
    "hosting",
    "hopping",
    "hop",
    "party",
    "serverhopping",
    "need",
    "trading",
    "looking",
    "farm",
    "farms",
}

SYMBOLS = {",", "/", "\\", "\n", "|", "‘", "*", ")", "(", ":", ";", "!", "-", "#"}

California = {"cali", "cal", "california", "cl"}
Singapore = {"sg", "singapore", "west", "nwsg", "nw", "northwest", "north-west"}
Texas = {"tx", "texas", "tex", "texts"}
Oregon = {"or", "oregon", "org", "oregan", "oregeon"}
Hesse = {"hesse", "germany", "de", "gesse"}
Unknown = {"unknown", "unkown", "unk", "unknow", "ur"}
Holland = {"holland", "netherlands", "nl", "holand"}
Florida = {"fl", "florida"}
Washington = {"wa", "washington"}
India = {"india", "maharatasha", "maharashtra", "mahatrasha"}

# Create the client for the self-bot
bot = discord.Client(self_bot=True)


def speak(text, volume=0.4):
    engine = pyttsx3.init()
    engine.setProperty("volume", max(0.0, min(volume, 1.0)))
    engine.say(text)
    engine.runAndWait()


def speak_region(server_name, words, volume=0.4):
    words = set(words)

    if words & California:
        speak(server_name + " California")
    elif words & Singapore:
        speak(server_name + " North West Singapore")
    elif words & Texas:
        speak(server_name + " Texas")
    elif words & Oregon:
        speak(server_name + " Oregon")
    elif words & Hesse:
        speak(server_name + " Hesse Germany")
    elif words & Unknown:
        speak(server_name + " Unknown")
    elif words & Holland:
        speak(server_name + " Holland")
    elif words & Florida:
        speak(server_name + " Florida")
    elif words & Washington:
        speak(server_name + " Washington")
    elif words & India:
        speak(server_name + " India")
    else:
        speak(server_name + " No Region")


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


def check_boss(text):
    text = text.lower()
    if text != "":
        print(text)

        # Check for keywords
        clean_text = text
        for symbol in SYMBOLS:
            clean_text = clean_text.replace(symbol, " ")

        words = clean_text.split()
        found_keywords = KEYWORDS & set(words)
        banned = BANNED_KEYWORDS & set(words)

        if found_keywords and not banned:
            print(f"Keyword(s) {found_keywords} found")
            server_name = find_correct_words(words)

            if server_name:
                pyperclip.copy(server_name)
                print("Server Name: " + YELLOW + server_name + RESET)
                speak_region(server_name, words)

        print("--------------------------------------------------")


@bot.event
async def on_ready():
    # print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print("--------------------------------------------------")
    print("Starting server sniper...")
    print("Logged in Successfully")
    print("--------------------------------------------------")
    print("--------------------------------------------------")


@bot.event
async def on_message(message):

    # print(f"Message detected in channel {message.channel.id} from {message.author}: {message.content}")

    # Ignore own messages to avoid loops
    if message.author == bot.user:
        return

    # Check if the message is in the source channel and has attachments
    if message.channel.id == SOURCE_CHANNEL_ID:
        check_boss(message.content)


bot.run(TOKEN)
