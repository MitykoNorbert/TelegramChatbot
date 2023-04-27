"""
Ez a modul a main függvényt tartalmazza,
illetve itt hívjuk meg a python-telegram-bot által
használt csomagokat.
"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import api_key as keys
import base_valaszok as R
from appointment_handler import AppointmentHandler
from appointment_session import AppointmentSession
from panasz_session import PanaszSession

sessions = {}
panasz = {}
appointmentHandler = AppointmentHandler()
appointmentHandler.load_appointments()
appointmentHandler.remove_old_appointments()
appointmentHandler.create_missing_appointments()


def start_command(update, context):
    """
    A beszélgetés kezdetén fut le.
    :param update:  telegram package által használt adatokat tartalmazza
    :param context: telegram package változó
    """
    print(str(update) + " + " + str(context) + " Conversation started")
    update.message.reply_text('Type something')


def help_command(update, context):
    """
    A /help parancs válaszreakciója
    :param update: telegram package által használt adatokat tartalmazza
    :param context: Chattel kapcsolatos információk
    :return:
    """
    update.message.reply_text('Üdv a Helper Bot Chatbot beszélgetésében!\n'
                              'Az alábbi parancsokat és kulcsszavakat tudod használni\n'
                              '/start - a beszélgetés indításához\n'
                              '/help - a funkciók felsorolásához\n'
                              'időpont - Időpont foglalási interakció indítása\n'
                              'foglal - Időpont foglalás\n'
                              'töröl - Időpont törlés\n'
                              'áttekint - Időpontjaid áttekintése\n'
                              'óra - A pontos idő és dátum\n'
                              'kicsoda - Rövid leírás a Helper Bot chatbotról\n'
                              'panasz - Ha meg szeretnél osztani velünk valamilyen problémát\n')
    if context.error is not None:
        error(update, context)


def handle_message(update, context):
    """
    Az üzenetet először kezelő függvény, ez kiegészíti az adatokat és
    paraméterekkel átadja a kezelő funkcióknak
    :param update: telegram package belső változója
    :param context: telegram package belső változója
    :return: a válasz üzenet
    """
    text = str(update.message.text).lower()
    username = update.message.from_user.username
    if username not in sessions:
        sessions[username] = AppointmentSession(appointmentHandler, username)
    session = sessions[username]
    if username not in panasz:
        panasz[username] = PanaszSession(False, username)
    response = R.sample_responses(text, username, session, panasz[username])

    update.message.reply_text(response)
    if context.error is not None:
        error(update, context)


def error(update, context):
    """
    Hiba kiíratás
    """
    print(f"Update {update} caused error {context.error}")


def main():
    """
    main függvény, itt kezeljük a telegram által érkező frissítést
    """
    updater = Updater(keys.API_KEY, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


main()
