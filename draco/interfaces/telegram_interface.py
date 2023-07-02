from typing import Mapping, Type, Any
from multiprocessing import Queue
import os
import keyring
import random
import datetime
import telepot
from telepot.loop import MessageLoop

class TelegramInterface(object):
    def __init__(
        self,
        config: Mapping[str, Any] = {},
        memory_proxy: tuple = (),
        telegram_queue: Queue = None,
        name: str = "telegram_bot"
    ) -> None:
        """
       Telegram interface constructor.

        Parameters
        ----------
        config : Mapping[str, Any]
            Class configuration map.
        memory_proxy: tuple
            system_status_proxy
            system_status_lock
        name : str
            json field name
        """
        config_draco = config.copy()
        if name in config:
            config_draco = config_draco[name]

        self._config = config_draco
        self.system_status_proxy = memory_proxy[0]
        self.system_status_lock = memory_proxy[1]
        self.telegram_queue = telegram_queue
        self.logging_chat_id = int(keyring.get_password(self._config["namespace"], self._config["user1"]))
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
            self._allowed_users = self._get_allowed_users(**self._config["allowed_users"])
            self._api_key = keyring.get_password(self._config["namespace"], self._config["api"])
            self._bot = telepot.Bot(self._api_key)
            MessageLoop(self._bot, self._handle).run_as_thread()
        except Exception as error:
            print(f"Process {self._pid} - " + repr(error))
            success = False
        return success
    
    def step_log(self) -> None:
        """
        This methods will check the queue and log the messages from other processes to self.logging_chat_id
        """
        try:
            msg = self.telegram_queue.get_nowait()
            self._bot.sendMessage(self.logging_chat_id, f"{msg}", parse_mode= "MarkdownV2")
        except Queue.empty:
            pass
    
    def _get_allowed_users(self, **kwargs):
        allowed = []
        for key in kwargs:
            allowed.append(int(keyring.get_password(self._config["namespace"], kwargs[key])))    
        return allowed
    
    def _handle(self, msg):
        chat_id = msg["chat"]["id"]
        command = msg["text"]
        if "@" in command: # to fix messages inside groups
            command = command.split("@")[0]
        if chat_id in self._allowed_users:
            print (f"Received command {command}")
            if command == "/random":
                self._bot.sendMessage(chat_id, random.randint(1,6))
            elif command == "/date":
                self._bot.sendMessage(chat_id, str(datetime.datetime.now()))
            elif command == "/photo":
                self._bot.sendPhoto(chat_id, "https://sklad500.ru/wp-content/uploads/2019/09/teleport02-1000x526.jpeg")
            elif command == "/status":
                self._check_status(chat_id)
            elif command == "/pump":
                self._toggle_pump(chat_id)
            elif command == "/valve1":
                self._toggle_valve(chat_id, 1)
            elif command == "/valve2":
                self._toggle_valve(chat_id, 2)
            elif command == "/valve3":
                self._toggle_valve(chat_id, 3)
    
    def _check_status(self, chat_id):
        """
        This method sends to the bot the system status data
        """
        self.system_status_lock.acquire()
        info = self.system_status_proxy._getvalue()
        self.system_status_lock.release()
        self._bot.sendMessage(chat_id, "*__System Status__*", parse_mode= "MarkdownV2")
        for key in info:
            self._bot.sendMessage(chat_id, f"{key}: {info[key]}")
    
    def _toggle_pump(self, chat_id):
        """
        This method toggle the value of the pump
        """
        self.system_status_lock.acquire()
        self.system_status_proxy["waterpump"] = int(not self.system_status_proxy["waterpump"])
        self._bot.sendMessage(chat_id, f"{__name__}: Request Pump Status to: {self.system_status_proxy['waterpump']}")
        self.system_status_lock.release()
    
    def _toggle_valve(self, chat_id, valve_number):
        """
        This method toggle the value of the valves 1, 2, 3
        """
        self.system_status_lock.acquire()
        self.system_status_proxy[f"valve{valve_number}"] = int(not self.system_status_proxy[f"valve{valve_number}"])
        self._bot.sendMessage(chat_id, f"{__name__}: Request Valve {valve_number} Status to: {self.system_status_proxy[f'valve{valve_number}']}")
        self.system_status_lock.release()
