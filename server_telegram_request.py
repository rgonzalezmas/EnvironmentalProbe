from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from w1thermsensor import W1ThermSensor
import Adafruit_DHT
import time
import params
import socket
import subprocess

sensor_ds18b20 = W1ThermSensor()
sensor_dht11 = Adafruit_DHT.DHT11
hostname = socket.gethostname()

time.sleep(30)

updater = Updater(params.token, use_context=True)

print ('Running ...')

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the Bot.Please write\
        /help to see the commands available.")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /temp - To get the temperature measure
    /hum - To get the humidity measure
    /sai - To get the UPS status""")

def temperature_measure(update: Update, context: CallbackContext):
    temperature = sensor_ds18b20.get_temperature()
    update.message.reply_text('Hi! I am the bot from {}. The temperature is: {}ºC '.format(hostname, temperature))

def humidity_measure(update: Update, context: CallbackContext):
    humidity, temp = Adafruit_DHT.read_retry(sensor_dht11, params.pin)
    update.message.reply_text('Hi! I am the bot from {}. The humidity is: {}% '.format(hostname, humidity))

def sai_status(update: Update, context: CallbackContext):
    command_status = "upsc sai_celler@localhost ups.status"
    ret_status = subprocess.run(command_status, capture_output=True, shell=True)
    estat = str(ret_status.stdout.decode())
    if estat == ('OL'):
        estat_ol = "on line"
        update.message.reply_text('Hi! I am the bot from {}. The UPS status is: {} '.format(hostname, estat_ol))
    elif estat == ('OB'):
        estat_ob = "on battery"
        update.message.reply_text('Hi! I am the bot from {}. The UPS status is: {} '.format(hostname, estat_ob))
    else:
        update.message.reply_text('Hi! I am the bot from {}. The UPS status is: {} '.format(hostname, estat))

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command. Type /help to see available commands." % update.message.text)

def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('temp', temperature_measure))
updater.dispatcher.add_handler(CommandHandler('hum', humidity_measure))
updater.dispatcher.add_handler(CommandHandler('sai', sai_status))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
