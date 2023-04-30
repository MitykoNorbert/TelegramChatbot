"""Ebben a modulban az időpont foglaláshoz
    szükséges munkamenet van megvalósítva
"""
from datetime import datetime
from appointment_handler import AppointmentHandler


class AppointmentSession:
    """Ez az osztály kezeli az időpontkezelés munkamenetét
               """

    def __init__(self, appointment_handler_instance: AppointmentHandler, username):
        """
             Args:
                  username (str): A chatbot által fogadott utolsó üzenet.
                  appointment_handler_instance (appointment_handler): Az időpontok kezeléséhez
                  szükséges osztály példánya.
                  step (str): A változó amely meghatározza, hogy a
                  folyamat melyik lépésénél tart a felhasználó.
                  extra_info: Ha egy folyamat esetén több lépés között szükséges
                  információt eltárolni, akkor itt tároljuk el.
             """
        self._step = "Prepared"
        self.appointment_handler_instance = appointment_handler_instance
        self._username = username
        self.extra_info = 0

    def reply_message(self, text):
        """Ez a függvény kezeli az időpontfoglalással kapcsolatos kéréseket

           Args:
               text (str): A chatbot által fogadott utolsó üzenet.

           Returns:
               str: A chatbot által küldendő válasz üzenet.

           """
        response = None
        if self._username is None:
            return "Ahhoz, hogy időpontokat rögzíthessünk a fiókodhoz, " \
                   "kérlek állíts be magadnak Telegram @felhasználónevet!"
        if text in ["quit", "cancel", "kilépés", "kilép"]:
            self._step = "Prepared"
            self.extra_info = 0
            return "Sikeresen megszakítottad az időpont foglalás interakciót."
        match self._step:
            case "Starting":
                response = "Ha időpontot szeretnél foglalni, vagy a " \
                           "meglévő időpontjaidat " \
                           "szeretnéd kezelni és áttekinteni, " \
                           "akkor kérlek válassz az alábbi opciók közül: \n" \
                           "Foglal - Ha szeretnél új időpontot foglalni \n" \
                           "Áttekint - Ha szeretnéd megtekinteni a " \
                           "saját időpontjaidat \n" \
                           "Töröl - Ha szeretnéd valamelyik " \
                           "időpontodat törölni"

                self._step = "OptionSelect"
            case "OptionSelect":
                match text:
                    case "foglal":
                        response = "Melyik napra szeretnél " \
                                   "időpontot foglalni?\n" \
                                   "Maximum 2 héten belül tudsz " \
                                   "időpontot foglalni\n" \
                                   "(YYYY/MM/DD)"
                        self._step = "DaySelect"
                    case "áttekint":

                        appointments = \
                            self.appointment_handler_instance.find_appointment_by_name(self._username)

                        response = "Az általad lefoglalt időpontok:\n"
                        for current_appointment in appointments:
                            response += str(current_appointment)
                    case "töröl":
                        appointments = []
                        appointments = self.appointment_handler_instance. \
                            find_appointment_by_name(self._username)
                        if len(appointments) == 1:
                            response = "Jelenleg 1 rögzített " \
                                       "időpontod van:\n" \
                                       "" + str(appointments[0]) + "\n" \
                                                                   "Szeretnéd törölni? \n" \
                                                                   "Igen / Nem"
                            self._step = "Delete1"
                        else:
                            response = "Melyik időpontodat " \
                                       "szeretnéd törölni?\n"
                            i = 0
                            for current_appointment in appointments:
                                i += 1
                                response += str(i) + " - " + str(current_appointment)
                            response += "Kérjük add meg a " \
                                        "sorszámát az időpontnak, " \
                                        "amelyet törölni szeretnél."
                            self._step = "DeleteSelect"

                    case _:
                        response = "Ezt a választ sajnos nem " \
                                   "tudtam értelmezni, " \
                                   "kérlek az alábbiak közül válassz:\n" \
                                   "Foglal - Ha szeretnél új " \
                                   "időpontot foglalni \n" \
                                   "Áttekint - Ha szeretnéd megtekinteni " \
                                   "a saját időpontjaidat \n" \
                                   "Töröl - Ha szeretnéd valamelyik " \
                                   "időpontodat törölni"
            case "DeleteSelect":
                try:
                    number = int(text)
                    appointments = []
                    appointments = self.appointment_handler_instance. \
                        find_appointment_by_name(self._username)
                    if number > len(appointments):
                        response = "Nincs ilyen sorszámú időpont, " \
                                   "próbáld újra! " \
                                   "(1 - " + str(len(appointments)) + ")"
                    else:
                        if self.appointment_handler_instance. \
                                del_by_user_and_id(self._username, number - 1):
                            response = "Sikeresen töröltük a " \
                                       "kiválasztott időpontot!\n" \
                                       "Interakció befejezve."
                            self.appointment_handler_instance. \
                                save_appointments()
                            self._step = "Prepared"
                        else:
                            response = "Valami hiba történt, " \
                                       "kérjük próbáld újra.."
                except ValueError:
                    response = "Kérjük, egy számot adj meg " \
                               "a felsorolt sorszámok közül!"
            case "Delete1":
                if text == "igen":
                    self.appointment_handler_instance. \
                        del_all_from_user(self._username)
                    response = "Az időpontot töröltük.\n" \
                               "Interakció vége"
                    self.appointment_handler_instance.save_appointments()
                else:
                    response = "Az időpont törlése megszakadt.\n" \
                               "Interakció vége"
                self._step = "Prepared"

            case "DaySelect":
                try:
                    date = datetime.strptime(text, '%Y/%m/%d')
                    response = "Az adott napon elérhető időpontok:\n"
                    frees = []
                    frees = self.appointment_handler_instance. \
                        get_free_appointments(date)
                    if len(frees) == 0:
                        response = "Sajnos ezen a napon jelenleg " \
                                   "nincs elérhető időpont. \n" \
                                   "Kérlek válassz másik napot. (YYYY/MM/DD)"
                    else:
                        i = 1
                        for current_appointment in frees:
                            response += str(i) + " - " + \
                                        str(current_appointment)
                            i += 1
                        response += "kérlek válaszolj az általád választott " \
                                    "időpont sorszámával.\n" \
                                    "(1 - " + str(len(frees)) + ")"
                        self._step = "AppointmentSelect"
                        self.extra_info = date
                except Exception:
                    response = "Hibás a dátum formátuma, próbáld újra!"

            case "AppointmentSelect":
                try:
                    date = self.extra_info
                    number = int(text)
                    frees = []
                    frees = self.appointment_handler_instance. \
                        get_free_appointments(date)
                    if number > len(frees):
                        response = "Nincs ilyen sorszámú időpont, " \
                                   "próbáld újra! (1 - " + \
                                   str(len(frees)) + ")"
                    else:
                        if self.appointment_handler_instance. \
                                foglalas(frees[number - 1], self._username):
                            response = "Sikeresen foglaltuk a " \
                                       "kiválasztott időpontot!\n" \
                                       "Interakció befejezve."
                            self.appointment_handler_instance. \
                                save_appointments()
                            self._step = "Prepared"
                        else:
                            response = "Valami hiba történt, " \
                                       "kérjük próbáld újra.."
                except ValueError:
                    response = "Kérjük, egy számot adj meg a" \
                               " felsorolt sorszámok közül!"
            case _:
                response = "Valami hiba történt"
                self._step = "Prepared"

        return response

    def set_step(self, step):
        """Setter metódus
            Args:
                step: az adott lépés, ahol a folyamat tart"""

        self._step = step

    def get_step(self):
        """Getter metódus  """
        return self._step
