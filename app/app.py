# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false

import threading
from tkinter import filedialog
from typing import Any, Callable

import customtkinter as ctk

from services import GeminiChatBot, GitHubScraper
from services.scraper import GitHubUserNotFound
from utils.export import export_to_excel
from utils.text import strip_md

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("app/theme.json")
FONT: tuple[str, int] = ("JetBrains Mono", 13)


class App(ctk.CTk):
    """main application window - contains github scraper and gemini chatbot UI."""

    def __init__(self):
        super().__init__()

        self.geometry("960x800")
        self.title("GitHub Repo Scraper + ChatBot")

        self.scraper: GitHubScraper = GitHubScraper()
        self.bot: GeminiChatBot | None = None
        self.repos: list[str] = []

        self.scraper_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        self.scraper_frame.pack(fill="x", padx=20, pady=10)
        self.chatbot_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        self.chatbot_frame.pack(fill="x", padx=20, pady=10)

        self.build_scraper_section()
        self.build_chatbot_section()

    def build_scraper_section(self):
        """builds github username input, filepath input, and search button"""
        self.githubLabel: ctk.CTkLabel = ctk.CTkLabel(
            self.scraper_frame, text="github username:", corner_radius=0, font=FONT
        )
        self.githubLabel.pack()

        self.githubTextbox: ctk.CTkEntry = ctk.CTkEntry(
            self.scraper_frame, width=480, corner_radius=0, font=FONT
        )
        self.githubTextbox.pack()

        self.fileLabel: ctk.CTkLabel = ctk.CTkLabel(
            self.scraper_frame, text="file path:", corner_radius=0, font=FONT
        )
        self.fileLabel.pack()

        self.fileTextbox: ctk.CTkEntry = ctk.CTkEntry(
            self.scraper_frame, width=480, corner_radius=0, font=FONT
        )
        self.fileTextbox.pack()

        self.button: ctk.CTkButton = ctk.CTkButton(
            self.scraper_frame,
            text="start search",
            command=self._run_scraper,
            corner_radius=0,
            font=FONT,
        )
        self.button.pack()

    def build_chatbot_section(self):
        """builds chat history display, message input, send button"""
        self.chatBox: ctk.CTkTextbox = ctk.CTkTextbox(
            self.chatbot_frame, width=800, height=300, font=FONT
        )
        self.chatBox.pack()
        self.chatBox.configure(state="disabled")

        self.chatEntry: ctk.CTkEntry = ctk.CTkEntry(
            self.chatbot_frame, width=600, font=FONT
        )

        self.chatEntry.pack()

        self.sendButton: ctk.CTkButton = ctk.CTkButton(
            self.chatbot_frame, text="ask gemini", command=self._ask_bot, font=FONT
        )

        self.sendButton.pack()

    def _run_scraper(self):
        """validates inputs, then scrapes repos and initialises chatbot in background thread"""
        username = self.githubTextbox.get().strip()
        path = self.fileTextbox.get().strip()
        if not username:
            return

        if not path:
            path = filedialog.asksaveasfilename(
                defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
            )
        if not path:
            return
        self.set_ui_busy(True)
        self.write_chat("scraping...")

        def task(username: str = username, path: str = path):

            print("scraping")
            try:
                repos = self.scraper.get_repos(username)

                if path:
                    export_to_excel(path, repos, username)

                def update_ui():
                    self.repos = repos
                    self.bot = GeminiChatBot(repos)
                    self.write_chat(f"loaded {len(repos)} repos for {username}")
                    self.set_ui_busy(False)

                self.after(0, update_ui)
            except GitHubUserNotFound as e:
                error_msg = str(e)

                def update_ui():
                    self.write_chat(error_msg)
                    self.set_ui_busy(False)

                self.after(0, update_ui)

        self.run_in_thread(task)

    def _ask_bot(self):
        """sends current chat entry to the chatbot in a background thread"""
        if not self.bot:
            self.write_chat("run scraper first")
            return

        question = self.chatEntry.get().strip()
        if not question:
            return
        self.chatEntry.delete(0, "end")
        self.write_chat(f"\n> you: {question}")
        self.write_chat("\nwaiting for response...")
        self.set_ui_busy(True)

        def task(question: str = question):
            if self.bot is None:
                return

            response = self.bot.ask(question)
            if response is None:
                response = ""

            def update_ui():
                self.write_chat(f"\n> gemini: {strip_md(response)}")
                self.set_ui_busy(False)

            _ = self.after(0, update_ui)

        self.run_in_thread(task)

    def write_chat(self, text: str):
        """appends text to chat display - safe to call from MAIN THREAD ONLY"""
        self.chatBox.configure(state="normal")
        self.chatBox.insert("end", text + "\n")
        self.chatBox.configure(state="disabled")

    def run_in_thread(self, func: Callable[[], Any]):
        """runs a callable in a daemon thread."""
        threading.Thread(target=func, daemon=True).start()

    def set_ui_busy(self, busy: bool):
        """disables or emabled interactive UI elements during background tasks."""
        state = "disabled" if busy else "normal"
        self.button.configure(state=state)
        self.sendButton.configure(state=state)
