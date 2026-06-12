# pyright: reportUnknownMemberType=false

from app import App
from scraper import GitHubScraper
import utils

if __name__ == "__main__":
    # app: App = App()
    # app.mainloop()
    ghs: GitHubScraper = GitHubScraper()
    utils.export_to_excel("test.xlsx", ghs.get_repos("iamzainrizwan"), "iamzainrizwan")
