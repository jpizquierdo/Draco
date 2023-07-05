import time
import random
import datetime
import telepot

# import board
# import adafruit_dht
from telepot.loop import MessageLoop

# from pprint import pprint
# import pandas as pd
import keyring

API_KEY = keyring.get_password("draco", "TELEGRAM_API_KEY")
USER_ID = int(keyring.get_password("draco", "CHAT_ID_USER1"))
GROUP_ID = int(keyring.get_password("draco", "CHAT_ID_GROUP1"))


def allowed_users(*args):
    allowed = []
    for item in args:
        allowed.append(item)
    return allowed


allowed = allowed_users(USER_ID, GROUP_ID)
# DHT11 temperature and humidity sensor:
# https://github.com/adafruit/Adafruit_CircuitPython_DHT

# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT11(board.D4)
# df = pd.DataFrame(columns=['Date', 'Temperature', 'Humidity'])


# ~ def get_DHT():
# ~ temperature_c = None
# ~ while temperature_c == None:
# ~ try:
# ~ # Print the values to the serial port
# ~ temperature_c = dhtDevice.temperature
# ~ #emperature_f = temperature_c * (9 / 5) + 32
# ~ humidity = dhtDevice.humidity
# ~ return temperature_c, humidity
# ~ except RuntimeError as error:
# ~ # Errors happen fairly often, DHT's are hard to read, just keep going
# ~ print(error.args[0])
# ~ time.sleep(2.0)
# ~ continue
# ~ except Exception as error:
# ~ dhtDevice.exit()
# ~ raise error


def handle(msg):
    global df
    chat_id = msg["chat"]["id"]
    command = msg["text"]
    # pprint(msg)
    if chat_id in allowed:
        print("Got command: %s" % command)
        if command == "/random":
            bot.sendMessage(chat_id, random.randint(1, 6))
        elif command == "/date":
            bot.sendMessage(chat_id, str(datetime.datetime.now()))
        elif command == "/photo":
            bot.sendPhoto(
                chat_id,
                "https://sklad500.ru/wp-content/uploads/2019/09/teleport02-1000x526.jpeg",
            )
        # elif command == '/status':
        # current_temperature, current_humidity=get_DHT()
        # bot.sendMessage(chat_id, "Temperature: "+str(current_temperature)+" ºC")
        # bot.sendMessage(chat_id, "Humedad: "+str(current_humidity)+" %")
        # df = df.append({'Date': str(datetime.datetime.now()), 'Temperature': current_temperature, 'Humidity': current_humidity}, ignore_index=True)
        # elif command == '/save':
        # print("Logging content: ", df, sep='\n')
        # df.to_csv("datos.csv",index = False)


bot = telepot.Bot(API_KEY)
MessageLoop(bot, handle).run_as_thread()
print("I am listening ...")
while 1:
    time.sleep(10)
