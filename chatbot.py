# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

from google import genai
from google.genai.chats import Chat
from config import GEMINI_API_KEY


class GeminiChatBot:
    def __init__(self, repos: list[str]) -> None:
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        repo_text = ", ".join(repos)
        self.chat: Chat = self.client.chats.create(model="gemini-3.5-flash")
        response = self.chat.send_message(f"""
        You are an assisstant that analyses GitHub repositories to screen programming experience for a Data Scientist role.

        You MUST ONLY use the repository names provided below. 

        Repositories:
        {repo_text}
        """)
        print(response.text)

    def ask(self, question: str) -> str | None:
        response = self.chat.send_message(question)
        return response.text
