import customtkinter as ctk
import threading
import asyncio
import discord
import pyperclip

# Initialize customtkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class DiscordBot(discord.Client):
    def __init__(self, gui):
        super().__init__(self_bot=True)
        self.gui = gui

    async def on_ready(self):
        self.gui.log("Logged in Successfully")
        self.gui.update_status("Running")

    async def on_message(self, message):
        if (
            message.author != self.user
            and message.channel.id == self.gui.source_channel_id
        ):
            pyperclip.copy(message.content)
            self.gui.log(f"Copied: {message.content}")


class BotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Server Sniper")
        self.geometry("800x500")

        # Status Label
        self.status_label = ctk.CTkLabel(
            self, text="Status: Stopped", font=("Arial", 16)
        )
        self.status_label.pack(pady=10)

        # Start/Stop Buttons
        self.start_button = ctk.CTkButton(
            self, text="Start Bot", command=self.start_bot
        )
        self.start_button.pack(pady=5)
        self.stop_button = ctk.CTkButton(
            self, text="Stop Bot", state="disabled", command=self.stop_bot
        )
        self.stop_button.pack(pady=5)

        # Log Box
        self.log_box = ctk.CTkTextbox(self, height=200, wrap="none")
        self.log_box.pack(pady=10, fill="both", expand=True)

        # Bot Instance
        self.bot = None
        self.bot_thread = None
        self.source_channel_id = 123412341234  # Replace with actual channel ID
        self.token = self.read_token()

    def read_token(self):
        with open("token.txt", "r") as file:
            return file.read().strip()

    def log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.yview_moveto(1)

    def update_status(self, status):
        self.status_label.configure(text=f"Status: {status}")

    def run_bot(self):
        asyncio.run(self.bot.start(self.token))

    def start_bot(self):
        if not self.bot:
            self.bot = DiscordBot(self)
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.update_status("Starting...")

    def stop_bot(self):
        if self.bot:
            asyncio.run_coroutine_threadsafe(self.bot.close(), self.bot.loop)
            self.bot = None
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.update_status("Stopped")
            self.log("Bot stopped")


if __name__ == "__main__":
    app = BotGUI()
    app.mainloop()
