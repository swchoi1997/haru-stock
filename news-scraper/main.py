import os

from dotenv import load_dotenv

from AppManager import AppManager


class NewsScraper:
    @staticmethod
    def load_env():
        load_dotenv()
        os.environ["GOOGLE_API_KEY"] = os.getenv("google_gemini_api_key")

    @staticmethod
    def run():
        NewsScraper.load_env()
        AppManager(app_name="scraper").run()


if __name__ == '__main__':
    NewsScraper.run()
