# pyright: reportUnknownMemberType=false

from app import App
from scraper import GitHubScraper

if __name__ == "__main__":
    # app: App = App()
    # app.mainloop()
    ghs: GitHubScraper = GitHubScraper()
    print(ghs.get_repos("iamzainrizwan"))
    print(ghs.get_repos("torvalds"))
