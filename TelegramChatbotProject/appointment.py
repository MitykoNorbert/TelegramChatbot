"""
Ebben a modulban van megvalósítva az Appointment class,
ami egy foglalható időpontot tárol el.
"""
from datetime import datetime


class Appointment:
    """
    Ebben az osztályban tároljuk az időpontokat
    """

    def __init__(self, date_time, is_free=True, name=None):
        """Appointment osztály konstruktora
                Args:
                    date_time (datetime):
                    A dátum és időpont,amelyre a foglalás történik
                    is_free (boolean): Szabad-e az adott időpont
                    name (string):
                    a felhasználónév, amely által foglalásra került az időpont
                    """

        self.date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')
        self.is_free = is_free
        self.name = name

    def get_date_time(self):
        """
        Getter
        :return: időpont ideje
        """
        return self.date_time

    def set_date_time(self, date_time):
        """
        Setter
        :param date_time: az időpont ideje
        """
        self.date_time = date_time

    def get_is_free(self):
        """
        getter metódus
        :return: Szabad-e az adott időpont
        """
        return self.is_free

    def set_is_free(self, is_free):
        """
        setter metódus
        :param is_free: Szabad-e az adott időpont
        """
        self.is_free = is_free

    def get_name(self):
        """getter a felhasználónévre, amire foglalás történik
            :return: A felhasználó neve"""
        return self.name

    def set_name(self, name):
        """setter a felhasználónévre, amire foglalás történik"""
        self.name = name

    def __repr__(self):
        """A json kezelés számára szükséges formátum megadása"""
        return f"Appointment({self.date_time.strftime('%Y.%m.%d %H:%M')}, " \
               f"{self.is_free}, {self.name})"

    def __str__(self):
        """To String metódus
                Itt adjuk meg, hogy milyen formában
                legyen egy időpont kiíratva.
                """
        if self.is_free:
            return f"({self.date_time.strftime('%Y.%m.%d %H:%M')}, " \
                   f"Szabad időpont)\n"
        return f"({self.date_time.strftime('%Y.%m.%d %H:%M')}, " \
               f"Foglalta:{self.name})\n"
