# github-scraper-chatbot

scrapes a GitHub user's public repositories and loads them into a Gemini-powered chatbot for analysis. built with CustomTkinter, BeautifulSoup, and the Google Generative AI SDK.

## what it does

- fetches all public repositories for a given GitHub username via HTML scraping (no API key required)
- exports the repository list to a `.xlsx` file
- initialises a Gemini chatbot with the repository list as context, allowing natural language queries about the user's work

## structure

```
├── app/            # UI — App class (CustomTkinter)
├── services/       # GitHubScraper, GeminiChatBot
├── utils/          # Excel export, markdown stripping
├── config.py       # API key handling
├── theme.json      # CustomTkinter colour theme
└── main.py         # Entry point
```

## setup

**1. clone and install dependencies**
```bash
git clone https://github.com/iamzainrizwan/github-scraper-chatbot
cd github-scraper-chatbot
uv sync
```

**2. set your Gemini API key**

get a free key at https://ai.google.dev, then copy `.env.example` to `.env` and fill in your key:
```bash
cp .env.example .env
```

make sure `.env` is in your `.gitignore`.

**3. run**
```bash
uv run main.py
```

## usage

1. enter a GitHub username
2. set a save location for the `.xlsx` file, or leave blank to use a file picker
3. click **start search** — repos are scraped, exported, and loaded into the chatbot
4. ask the chatbot anything about the repositories

## AI usage
AI tools were used only as a debugging aid and for clarifying library usage. no full solutions or architectural design decisions were sourced from AI. the final codebase was implemented, reviewed, and tested independently. 
