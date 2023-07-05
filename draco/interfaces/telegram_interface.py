from typing import Mapping, Any
from multiprocessing import Queue
import queue
import os
import keyring
import random
from functools import partial
import datetime
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


class TelegramInterface(object):
    def __init__(
        self,
        config: Mapping[str, Any] = {},
        memory_proxy: tuple = (),
        telegram_queue: Queue = None,
        name: str = "telegram_bot",
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
        telegram_queue : Queue
            telegram queue to send logging to main user
        name: str
            name in json file
        """
        config_draco = config.copy()
        if name in config:
            config_draco = config_draco[name]

        self._config = config_draco
        self.system_status_proxy = memory_proxy[0]
        self.system_status_lock = memory_proxy[1]
        self.telegram_queue = telegram_queue
        self.logging_chat_id = int(
            keyring.get_password(
                self._config["namespace"], self._config["allowed_users"]["user1"]
            )
        )
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
            self._allowed_users = self._get_allowed_users(
                **self._config["allowed_users"]
            )
            self._api_key = keyring.get_password(
                self._config["namespace"], self._config["api"]
            )
            # Create the Application and pass it your bot's token.
            self.application = Application.builder().token(self._api_key).build()
            # on different commands - answer in Telegram
            self.application.add_handler(
                CommandHandler(
                    command="status",
                    callback=self._check_status,
                    filters=filters.Chat(self._allowed_users),
                )
            )
            self.application.add_handler(
                CommandHandler(
                    command="pump",
                    callback=self._toggle_pump,
                    filters=filters.Chat(self._allowed_users),
                )
            )
            self.application.add_handler(
                CommandHandler(
                    command="valve1",
                    callback=partial(self._toggle_valve,valve_number=1),
                    filters=filters.Chat(self._allowed_users),
                )
            )
            self.application.add_handler(
                CommandHandler(
                    command="valve2",
                    callback=partial(self._toggle_valve,valve_number=2),
                    filters=filters.Chat(self._allowed_users),
                )
            )
            self.application.add_handler(
                CommandHandler(
                    command="valve3",
                    callback=partial(self._toggle_valve,valve_number=3),
                    filters=filters.Chat(self._allowed_users),
                )
            )
            self.application.add_handler(
                CommandHandler(
                    command="holidays",
                    callback=self._toggle_holidays,
                    filters=filters.Chat(self._allowed_users),
                )
            )
            # on non command i.e message - echo the message on Telegram
            self.application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, None)
            )
            # Run the bot until the user presses Ctrl-C
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as error:
            print(f"Process {self._pid} - " + repr(error))
            success = False
        return success

    async def step_log(self) -> None:
        """
        This methods will check the queue and log the messages from other processes to self.logging_chat_id
        """
        try:
            msg = self.telegram_queue.get_nowait()
            await self.application.bot.send_message(
                chat_id=self.logging_chat_id, text=msg
            )
        except queue.Empty:
            pass

    def _get_allowed_users(self, **kwargs):
        """
        Parse the dictionary from config file to read and append the allowed users.
        """
        allowed = []
        for key in kwargs:
            allowed.append(
                int(keyring.get_password(self._config["namespace"], kwargs[key]))
            )
        return allowed

    async def _check_status(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        This method sends to the bot the system status data
        """
        self.system_status_lock.acquire()
        info = self.system_status_proxy._getvalue()
        self.system_status_lock.release()
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )
        await update.message.reply_markdown("*__System Status__*")
        for key in info:
            update.message.reply_text(f"{key}: {info[key]}")

    async def _toggle_pump(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        This method toggle the value of the pump
        """
        self.system_status_lock.acquire()
        self.system_status_proxy["waterpump"] = int(
            not self.system_status_proxy["waterpump"]
        )
        update.message.reply_text(
            f"{__name__.split('.')[-1]}: Request Pump Status to {self.system_status_proxy['waterpump']}"
        )
        self.system_status_lock.release()

    async def _toggle_valve(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, valve_number
    ) -> None:
        """
        This method toggle the value of the valves 1, 2, 3
        """
        self.system_status_lock.acquire()
        self.system_status_proxy[f"valve{valve_number}"] = int(
            not self.system_status_proxy[f"valve{valve_number}"]
        )
        update.message.reply_text(
            f"{__name__.split('.')[-1]}: Request Valve {valve_number} Status to {self.system_status_proxy[f'valve{valve_number}']}"
        )
        self.system_status_lock.release()

    async def _toggle_holidays(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        This method toggle the value of the holidays mode
        """
        self.system_status_lock.acquire()
        self.system_status_proxy["holidays"] = int(
            not self.system_status_proxy["holidays"]
        )
        update.message.reply_text(
            f"{__name__.split('.')[-1]}: Request Holidays Mode to {self.system_status_proxy['holidays']}"
        )
        self.system_status_lock.release()
