"""
Ebben a modulban vannak a tesztek
"""
import unittest
from kerdes import Kerdes, SzuperKerdes
from szam_jatek import JatekSession
from appointment import Appointment
from appointment_session import AppointmentSession
from appointment_handler import AppointmentHandler


class ChatbotTester(unittest.TestCase):
    """Ebben az osztályban vannak a teszt függvényei"""
    def setUp(self):
        self.jatek_session = JatekSession()
        self.handler = AppointmentHandler()
        self.appointment_session = AppointmentSession(self.handler, "tester")

    def test_kerdes_konstruktor(self):
        """ A kérdés osztály konstruktorát teszteli"""
        kerdes = Kerdes()
        self.assertTrue(kerdes.text is not None)
        self.assertTrue(kerdes.valasz is not None)

    def test_tipp_kerdes_jo(self):
        """A helyes válasszal tesztel"""
        kerdes = Kerdes()
        self.assertTrue(kerdes.tippel(str(kerdes.valasz)))

    def test_tipp_kerdes_rossz(self):
        """Teszteli a helytelen válasszal"""
        kerdes = Kerdes()
        self.assertFalse(kerdes.tippel(str(kerdes.valasz - 1)))

    def test_szuperkerdes_konstruktor(self):
        """A szuperkérdés osztály létrehozását teszteli"""
        kerdes = SzuperKerdes()
        self.assertTrue(kerdes.text is not None)
        self.assertTrue(kerdes.valasz is not None)

    def test_tipp_szuperkerdes_jo(self):
        """A szuperkérdés osztály helyes válaszát teszteli"""
        kerdes = SzuperKerdes()
        self.assertTrue(kerdes.tippel(str(kerdes.valasz)))

    def test_tipp_szuperkerdes_rossz(self):
        """A szuperkérdés osztály helytelen válaszát teszteli"""
        kerdes = SzuperKerdes()
        self.assertFalse(kerdes.tippel(str(kerdes.valasz - 1)))

    def test_jatek_session_init(self):
        """A JátékSession létrehozását teszteli"""
        session = JatekSession()
        self.assertEqual(session.korszam, 1)
        self.assertEqual(session.pontok, 0)
        self.assertTrue(session is not None)

    def test_jatek_session_response1(self):
        """A játéksession válaszait teszteli"""
        self.jatek_session.response("játék")
        valasz = self.jatek_session.current_kerdes.valasz
        self.jatek_session.response(str(valasz))
        self.assertTrue(self.jatek_session.in_game)
        self.assertTrue(self.jatek_session.pontok > 0)

    def test_jatek_session_response2(self):
        """A játéksession válaszait teszteli"""
        expected = "Már játékban vagy! \n" \
                   "Ha ki szeretnél lépni a játékból," \
                   " írd be, hogy 'kilépés'"
        self.jatek_session.response("játék")
        self.assertEqual(self.jatek_session.response("játék"), expected)

    def test_jatek_session_response_quit(self):
        """A játéksession válaszait teszteli kilépéskor"""
        self.jatek_session.response("játék")
        self.jatek_session.response("kilépés")
        self.assertFalse(self.jatek_session.in_game)

    def test_appointment_session(self):
        """Több lépést is tesztel az appointment session osztályban"""
        self.assertEqual(self.appointment_session.get_step(), "Prepared")
        self.appointment_session.set_step("OptionSelect")
        self.appointment_session.reply_message("foglal")

        self.assertEqual(self.appointment_session.get_step(), "DaySelect")
        self.assertEqual(self.appointment_session.reply_message("hihihihahaha"),
                         "Hibás a dátum formátuma, próbáld újra!")
        expected = "Sajnos ezen a napon jelenleg " \
                   "nincs elérhető időpont. \n" \
                   "Kérlek válassz másik napot. (YYYY/MM/DD)"
        self.assertEqual(self.appointment_session.reply_message("2023/04/05"), expected)
        self.assertEqual(self.appointment_session.reply_message("kilépés"),
                         "Sikeresen megszakítottad az időpont foglalás interakciót.")
        self.appointment_session.set_step("OptionSelect")
        self.assertTrue(self.appointment_session.reply_message("áttekint") is not None)
        self.assertEqual(self.appointment_session.get_step(), "OptionSelect")
        self.assertTrue(self.appointment_session.reply_message("töröl") is not None)

    def test_handler_load(self):
        """Az időpontok betöltését teszteli"""
        appointments = self.handler.load_appointments()
        self.assertTrue(appointments is not None)

    def test_handler_find(self):
        """Időpontok keresését teszteli"""
        test_datetime = "2022-05-09T14:00:00"
        test_idopont = Appointment(test_datetime)
        self.handler.add_appointment(test_idopont)
        self.handler.foglalas(test_idopont, "tester")
        self.assertEqual(self.handler.find_appointment_by_name("tester"), [test_idopont])

    if __name__ == '__main__':
        unittest.main()
