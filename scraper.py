# scrape github profile for repos using BeautifulSoup to parse HTML
import requests
from bs4 import BeautifulSoup


# itemprop="name codeRepository"
class GitHubScraper:
    def get_repos(self, username: str) -> list[str]:
        repos: list[str] = []
        n = 1
        link = f"https://github.com/{username}?tab=repositories&page={n}"
        response: requests.Response = requests.get(link)

        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.select('[itemprop="name codeRepository"]')
        for e in elements:
            repos.append(e.text.strip())
        return repos
