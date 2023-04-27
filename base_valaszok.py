"""
Ebben a modulban található a válaszkezelés.
Itt dől el, hogy egyszerű kulcsszavakra milyen válasz érkezzen,
illetve, hogy szükséges-e tovább adni az üzenetet.
"""
from datetime import datetime

from panasz import Panasz


def sample_responses(input_text, user, session, panasz):
    """
    Ez a függvény kezeli a bejövő szöveges üzeneteket.
        Az egyszerű üzeneteket megválaszolja, a több lépéses folyamatokat pedig továbbadja
        a munkamenet kezelőfunkciójának.
    :param input_text: A beérkező szöveges üzenet a felhasználótól
    :param user: Az adott felhasználó felhasználóneve.
    :param session: A felhasználó munkamenete
    :return: Válaszüzenet a chatbottól
    """
    user_message = str(input_text).lower()
    username = str(user)
    response = None
    if panasz.panaszmode:
        if user_message == "mégse":
            panasz.panaszmode = False
            response = "A panasz felvétele megszakadt."

        else:
            reklamacio = Panasz(username, input_text)
            reklamacio.save()
            panasz.panaszmode = False
            response = "A panaszt rögzítettük"
        return response

    if session.get_step() == "Prepared" and user_message in (
            "appointment", "reservation", "appointment?", "időpontfoglalás", "időpont"):
        session.set_step("Starting")
    if user_message in ("foglal", "töröl", "áttekint"):
        session.set_step("OptionSelect")
    if session.get_step() != "Prepared":
        return session.reply_message(text=input_text)

    if user_message in ("hello", "hi", "sup", "szia", "halo", "hello", "heló"):
        response = "Szia! \n" \
                   "Miben tudok segíteni neked?"
    if user_message in ("who are you", "who are you?", "kicsoda", "ki vagy te?"):
        response = "Én egy Telegram chatbot vagyok, aki segít időpontokat felvenni egy rendszerbe"
    if user_message in ("time", "time?", "idő", "idő?", "az idő?", "óra"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")
        response = str(date_time)
    if user_message in ("reklamáció", "reklamációt", "panasz", "panaszt") or \
            "reklamáció" in user_message:
        panasz.panaszmode = True
        response = "Kérjük add meg egy üzenetben a problémát, amivel szembesültél.\n" \
                   "Ha mégsem szeretnél panaszt írni, akkor írd be a 'mégse' szót."
    if response is not None:
        return response
    return "Sajnálom " + username + ", viszont ezt nem tudtam értelmezni.\n" \
                                    "Kérlek használd a /help parancsot, ha " \
                                    "szeretnéd megtudni az elérhető funkcióim"
