"""Ebben a modulban az AppointmentHandler osztály és
a hozzá tartozó adatkezelő műveletek vannak megvalósítva
"""
import json
from datetime import datetime, timedelta

from appointment import Appointment


class AppointmentHandler:
    """
    Ebben az osztályban találhatóak az időpontok kezeléséért felelős függvények
    """

    def __init__(self, path):
        """Konstruktor
                    Args:
                        appointments[]: Az időpontokat tartalmazó tömb
                    """
        self.appointments = []
        self.path=path

    def add_appointment(self, appointment):
        """Adott időpont foglalását rögzítő függvény
                                Args:
                                    appointment (Appointment): Az adott időpont példánya,
                                    amelyet fel szeretnénk venni a listába.
                                """
        self.appointments.append(appointment)

    def foglalas(self, appointment, username):
        """Adott időpont foglalását rögzítő függvény
                        Args:
                            appointment (Appointment): Az adott időpont példánya,
                            amelyet le szeretnénk foglalni.
                            username (str): A foglalást rögzítő felhasználó neve
                        """
        try:
            appointment.name = username
            appointment.is_free = False
            return True
        except Exception:
            return False

    def remove_appointment(self, appointment):
        """Adott időpont foglalását eltávolító függvény
                Args:
                    appointment (Appointment): az adott időpont példánya, amelyről a
                    felhasználó le szeretné venni a foglalását.
                """
        appointment.name = None
        appointment.is_free = True

    def remove_old_appointments(self):
        """A múltbeli dátummal rendelkező időpontokat eltávolító függvény"""
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        old_appointments = []

        for appointment in self.appointments:
            if appointment.date_time < today:
                old_appointments.append(appointment)

        for appointment in old_appointments:
            self.appointments.remove(appointment)

    def create_missing_appointments(self):
        """ A következő 2 hét munkanapjait feltölti foglalható időpontokkal, ahol
        még nincs rögzítve."""
        today = datetime.now().date()
        end_date = today + timedelta(days=14)
        delta = timedelta(days=1)

        while today <= end_date:
            if today.weekday() >= 5:
                today += delta
                continue

            appointments_exist = False
            for appointment in self.appointments:
                if appointment.date_time.date() == today:
                    appointments_exist = True
                    break

            if not appointments_exist:
                for i in range(5):
                    appointment_time = datetime(today.year, today.month, today.day, 10 + i)
                    appointment_time_str = appointment_time.strftime('%Y-%m-%dT%H:%M:%S')
                    appointment = Appointment(appointment_time_str, True, None)
                    self.appointments.append(appointment)

            today += delta

    def find_appointment_by_name(self, name):
        """"Megkeresi az összes időpontot, ami egy felhasználó nevére lett regiszrálva
                Args:
                    name(str): A felhasználónév, amire keresünk.
                Returns:
                    appointments[]: Az összes adott névre regisztrált időpontból
                    összeállított tömb.
                """
        appointments = []
        for appointment in self.appointments:
            if appointment.name == name:
                appointments.append(appointment)
        return appointments

    def load_appointments(self):
        """Fájlból betölti az eltárolt időpontokat egy tömbbe"""
        filename = self.path+"/TelegramChatbotProject/Content/Appointments.json"
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            for appointment_data in data["appointments"]:
                appointment = Appointment(
                    appointment_data["date_time"],
                    appointment_data["is_free"],
                    appointment_data["name"]
                )
                self.appointments.append(appointment)
        appointments=self.appointments
        return appointments

    def get_free_appointments(self, date):
        """A még le nem foglalt időpontokat lekérő metódus
                :param date: A nap, amin keressük az elérhető időpontokat
                Returns:
                    free_appointments[]: Egy tömb, ami tartalmazza az adott nap
                    elérhető időpontjait."""
        free_appointments = []
        for appointment in self.appointments:
            if appointment.date_time.date() == date.date() and appointment.is_free:
                free_appointments.append(appointment)
        return free_appointments

    def save_appointments(self):
        """"Fájlba mentjük a változtatásokat az időpontokon
                Minden foglalás és törlés után mentünk, hogy ha bármilyen okból leáll a rendszer,
                a felhasználók változtatásai ne veszhessenek el."""
        filename = self.path+"/TelegramChatbotProject/Content/Appointments.json"
        data = {"appointments": []}
        for appointment in self.appointments:
            appointment_data = {
                "date_time": appointment.date_time.isoformat(),
                "is_free": appointment.is_free,
                "name": appointment.name
            }
            data["appointments"].append(appointment_data)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def del_by_user_and_id(self, username, number):
        """
        A felhasználó által kiválasztott időpont foglalás törlése
        :param username:A felhasználónév
        :param number:A felhasználó által választott sorszám, amelyet törölni kíván
        :return:A törlés sikeressége
        """
        try:
            appointments = []
            for current_appointment in self.appointments:
                if current_appointment.get_name() == username:
                    appointments.append(current_appointment)
            deleted = appointments[number]
            self.remove_appointment(deleted)
            return True
        except Exception as exception:
            print(exception)
            return False

    def del_all_from_user(self, username):
        """
        Egy adott felhasználó összes foglalását törli
        :param username: A felhasználónév
        """
        for current_appointment in self.appointments:
            if current_appointment.get_name() == username:
                self.remove_appointment(current_appointment)
