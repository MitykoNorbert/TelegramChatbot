"""
Ebben a modulban van megvalósítva a
számjátékot kezelő munkamenet osztálya
"""
from kerdes import Kerdes, SzuperKerdes


class JatekSession:
    """
    Ez az osztály kezeli a chatbot számjáték munkamentetét
    """

    def __init__(self):
        """
        Konstruktor a játék session osztályhoz.
        """
        self.korszam = 1
        self.pontok = 0
        self.in_game = False
        self.current_kerdes = None

    def response(self, input_text):
        """
        Itt történik a játék közbeni válaszok feldolgozása
        :param input_text:
        :return:
        """
        response = ""
        if input_text in ["kilépés", "quit", "kilép", "kilepes", "kilep"]:
            self.in_game = False
            return "Sikeresen kiléptél a játékból"
        match input_text:
            case "játék":
                if self.in_game:
                    response = "Már játékban vagy! \n" \
                               "Ha ki szeretnél lépni a játékból," \
                               " írd be, hogy 'kilépés'"
                else:
                    self.in_game = True
                    self.current_kerdes = Kerdes()
                    response = "Játék elindítva!\n" \
                               "Ha ki szeretnél lépni a játékból," \
                               " írd be, hogy 'kilépés'\n"
                    response += self.current_kerdes.text

            case _:
                if self.current_kerdes.tippel(input_text):
                    if isinstance(self.current_kerdes, SzuperKerdes):
                        self.pontok += 3
                    else:
                        self.pontok += 1
                    response = "Helyes válasz!\n" \
                               "Jelengleg " + str(self.pontok) + " pontod van!\n " \
                                                                 "Következő kérdés:\n"
                else:
                    self.pontok = 0
                    response = "Helytelen válasz.\n" \
                               "A pontszámod nullázódott.\n" \
                               "A helyes válasz: " \
                               "" + str(self.current_kerdes.valasz) + " volt." \
                                                                      "Következő kérdés:\n"
                if self.korszam % 5 == 0:
                    self.current_kerdes = SzuperKerdes()
                else:
                    self.current_kerdes = Kerdes()
                self.korszam += 1
                response += self.current_kerdes.text
        return response
