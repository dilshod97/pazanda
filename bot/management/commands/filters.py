from telegram.ext import BaseFilter


class FilterLanguage(BaseFilter):
    def filter(self, message):
        return message.text in ['🇺🇿 UZ', '🇷🇺 RU']