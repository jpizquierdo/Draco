from typing import Mapping, Type, Any
import os
import keyring
import random
import datetime
import telepot

class TelegramInterface(object):
    def __init__(
        self,
        config: Mapping[str, Any] = {}
    ) -> None:
        """
       Telegram interface constructor.

        Parameters
        ----------
        config : Mapping[str, Any]
            Class configuration map.
        """
        config_draco = config.copy()
        if "telegram_bot" in config:
            config_draco = config_draco["telegram_bot"]

        self._config = config_draco
        self._pid = os.getpid()
        self._allowed_users = []
        self._api_key = ""

   
    def init(
        self,
    ) -> bool:
        """
        This public function initialises the connection with the telegram bot.

        Returns
        -------
        success : bool
            True if successful initialisation, False otherwise.
        """

        success = True

        try:
            self.allowed_users = self._get_allowed_users(**self._config["allowed_users"])
            self._api_key = keyring.get_password(self._config["namespace"], self._config["api"])
            bot = telepot.Bot(self._api_key)
            telepot.loop.MessageLoop(bot, self._handle).run_as_thread()
        except Exception as error:
            print(f"Process {self._pid} - " + repr(error))
            success = False

        return success
    
    def _get_allowed_users(self, **kwargs):
        allowed = []
        for key in kwargs:
            allowed.append(int(keyring.get_password(self._config["namespace"], kwargs[key])))    
        return allowed
    
    def _handle(self, msg):
        chat_id = msg["chat"]["id"]
        command = msg["text"]
        if chat_id in self._allowed_users:
            print (f"Received command {command}")
            if command == "/random":
                bot.sendMessage(chat_id, random.randint(1,6))
            elif command == "/date":
                bot.sendMessage(chat_id, str(datetime.datetime.now()))
            elif command == "/photo":
                bot.sendPhoto(chat_id, "https://sklad500.ru/wp-content/uploads/2019/09/teleport02-1000x526.jpeg")