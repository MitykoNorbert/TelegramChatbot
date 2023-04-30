"""
Ebben a modulban a panaszkezeléshez szükséges
Panasz osztályt valósítjuk meg.
"""
from datetime import datetime


class Panasz:
    """
    A panasz osztályban rögzítjük a felhasználó által
    felvett panaszt.
    """

    def __init__(self, username, text):
        """

        :param username:  felhasználónév
        :param text:    A panasz tartalma
        """
        self.username = username
        self.text = text
        self.ido = datetime.now()

    def save(self):
        """
        A panaszt file-ba mentő függvény
        """

        filename = f"TelegramChatbotProject/Reklamaciok/{self.username}-{self.ido.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"{str(self.username)}\n{self.text}\n")

    def get_text(self):
        """Getter a szöveg tartalmához."""
        return self.text
