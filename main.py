# pyright: reportUnknownMemberType=false

from app import App
from scraper import GitHubScraper
from chatbot import GeminiChatBot
import utils

if __name__ == "__main__":
    # app: App = App()
    # app.mainloop()
    ghs: GitHubScraper = GitHubScraper()
    gcb: GeminiChatBot = GeminiChatBot(ghs.get_repos("torvalds"))
    utils.export_to_excel("test.xlsx", ghs.get_repos("torvalds"), "torvalds")
    print(gcb.ask("who's github is this?"))
