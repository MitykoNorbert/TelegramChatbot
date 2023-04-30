"""
Ebben a modulban a panaszkezeléshez szükséges munkamenet
van megvalósítva.
"""


class PanaszSession:
    """Referencia objektum a panasz munkamenetének eltárolásához"""

    def __init__(self, value, username):
        """
        Konstruktor
        :param value:Boolean érték, a munkamenet aktivitását jelzi.
        :param username: felhasználónév, ami a munkamenethez tartozik.
        """
        self.panaszmode = value
        self.username = username

    def get_value(self):
        """
        :return: boolean érték, ami a munkamenethez tartozik.
        """
        return self.panaszmode

    def get_username(self):
        """
        :return: felhasználév, ami a munkamenethez tartozik.
        """
        return self.username
