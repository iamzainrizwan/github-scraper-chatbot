# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownMemberType=false

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("theme.json")
FONT: tuple[str, int] = ("JetBrains Mono", 13)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("960x800")
        self.title("github repo scraper")
        self.build_scraper_section()

    def build_scraper_section(self):
        self.githubLabel: ctk.CTkLabel = ctk.CTkLabel(
            self, text="github username:", corner_radius=0, font=FONT
        )
        self.githubLabel.pack()

        self.githubTextbox: ctk.CTkEntry = ctk.CTkEntry(
            self, width=480, corner_radius=0, font=FONT
        )
        self.githubTextbox.pack()

        self.fileLabel: ctk.CTkLabel = ctk.CTkLabel(
            self, text="file path:", corner_radius=0, font=FONT
        )
        self.fileLabel.pack()

        self.fileTextbox: ctk.CTkEntry = ctk.CTkEntry(
            self, width=480, corner_radius=0, font=FONT
        )
        self.fileTextbox.pack()

        self.button: ctk.CTkButton = ctk.CTkButton(
            self,
            text="start search",
            command=self._run_scraper(),
            corner_radius=0,
            font=FONT,
        )
        self.button.pack()

    def build_chatbot_section(self):
        # TODO
        pass

    def _run_scraper(self):
        print("button clicked!")
