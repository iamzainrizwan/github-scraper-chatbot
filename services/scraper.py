# scrape github profile for repos using BeautifulSoup to parse HTML
import requests
from bs4 import BeautifulSoup


class GitHubUserNotFound(Exception):
    """raised when a github username does not exist"""

    pass


# itemprop="name codeRepository"
class GitHubScraper:
    """scrapes public repos from a github user's profile page"""

    def __init__(self) -> None:
        self.headers = {"User-Agent": "github-scraper-chatbot"}
        self.session = requests.session()

    def get_repos(self, username: str) -> list[str]:
        """fetches all public repo names for a given github username

        paginates through the repos tab until no more  results are found.
        raises GitHubUserNotFound if profile 404s
        """
        repos = []

        profile = f"https://github.com/{username}"
        response = self.session.get(profile, headers=self.headers, timeout=10)

        if response.status_code == 404:
            raise GitHubUserNotFound(f"gitHub user {username} does not exist")
        n = 1
        while True:
            link = f"https://github.com/{username}?tab=repositories&page={n}"
            response = self.session.get(link, headers=self.headers, timeout=10)

            soup = BeautifulSoup(response.text, "html.parser")
            repo_elements = soup.select('[itemprop="name codeRepository"]')

            if not repo_elements:
                break

            for e in repo_elements:
                repos.append(e.text.strip())

            n += 1

        return repos
