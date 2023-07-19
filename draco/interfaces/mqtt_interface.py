from typing import Mapping, Any
from multiprocessing import Queue
import os
import paho.mqtt.client as mqtt


class MQTTInterface(object):
    def __init__(
        self,
        config: Mapping[str, Any] = {},
        memory_proxy: tuple = (),
        telegram_queue: Queue = None,
        name: str = "mqtt",
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
        self._pid = os.getpid()
        self.client = None

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        info = self._check_status()
        for key in info:
            client.subscribe(f"home/watering/{key}")
        client.subscribe(f"home/watering/available")

    def on_message(self, client, userdata, message):
        print(
            "received message: ",
            str(message.payload.decode("utf-8")),
            "from ",
            message.topic,
        )
        self.system_status_lock.acquire()
        self.system_status_proxy[message.topic.split("/")[-1]] = int(message.payload)
        self.system_status_lock.release()

    def init(
        self,
    ) -> bool:
        """
        This public function initialises the mqtt device.

        Returns
        -------
        success : bool
            True if successful initialisation, False otherwise.
        """
        success = True
        try:
            self.client = mqtt.Client(client_id="Draco", protocol=mqtt.MQTTv5)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(
                host=self._config["broker_ip"], port=self._config["broker_port"]
            )
            self.client.loop_start()
            self.client.publish(
                topic=f"home/watering/available", payload="1", retain=True
            )

        except Exception as error:
            print(f"Process {self._pid} - " + repr(error))
            success = False
        return success

    def step(self) -> None:
        """
        This methods will check status and publish to the broker the current state
        """
        info = self._check_status()
        for key in info:
            self.client.publish(
                topic=f"home/watering/{key}", payload=info[key], retain=True
            )

    def _check_status(self):
        """
        This method check the system status proxy
        """
        self.system_status_lock.acquire()
        info = self.system_status_proxy._getvalue()
        self.system_status_lock.release()
        return info

    def _log(self, msg):
        """
        Logging function that queues message for telegram
        #TODO: will implement a python logger
        """
        self.telegram_queue.put(f"{__name__.split('.')[-1]}: {msg}")
