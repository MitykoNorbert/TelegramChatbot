"""
Ebben a modulban vannak megvalósítva a Kérdés osztályok.
"""
import random


class Kerdes:
    """
    Ebben az osztályban vannak megvalósítva a szám játék kérdései
    """

    def __init__(self):
        """
        Konstruktor, létrehozza a kérdés szövegét, és a helyes választ tároló változót
        """
        self.valasz = 0
        self.text = self.kerdest_general()

    def kerdest_general(self):
        """
        Generál egy egyszerű kérdést
        :return: A kérdés szövege.
        """
        num1 = random.randint(10, 1000)
        num2 = random.randint(10, 1000)
        self.valasz = num1 + num2
        return "Mennyi " + str(num1) + " + " + str(num2) + "?"

    def tippel(self, tipp):
        """
        Ellenőrzi, hogy a felhasználó által adott input helyes válasz-e
        :param tipp: a felhasználó által adott válasz
        :return: Helyes-e a megoldás
        """
        if tipp == str(self.valasz):
            return True
        return False


class SzuperKerdes(Kerdes):
    """
    Ebben az osztályban a Kérdés egy gyermekosztálya van megvalósítva,
    Ami egy összetettebb kérdést tartalmaz
    """

    def kerdest_general(self):
        """
        A kérdés generálás felül van írva, olyan módon, hogy különböző típusú
        kérdést generáljon.
        :return: A kérdés szövege.
        """
        num1 = random.randint(10, 1000)
        num2 = random.randint(10, 1000)
        num3 = random.randint(10, 100)
        num4 = random.randint(10, 100)
        self.valasz = (num1 * num3) + (num2 * num4)
        return "Mennyi " + str(num1) + " * " + str(num3) + " + " + str(num2) + " * " + str(num4) + "?"
