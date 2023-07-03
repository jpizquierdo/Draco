import sys, os
from pathlib import Path
from multiprocessing import Manager, Queue
from draco.processors.telegram_bot import TelegramBot
from draco.processors.GPIO_handler import GPIOHandler
from draco.processors.system_scheduler import SystemScheduler
from draco.utils.types import Status
import argparse
import json
import RPi.GPIO as GPIO
from time import sleep


def main(manager) -> int:
    success = True
    processes = None
    pid = os.getpid()
    GPIO.cleanup() # cleanup will be made in main application only
    try:
        # Get static configuration for the program
        parser = argparse.ArgumentParser()
        parser.add_argument(
        "-c", "--config",
        default="config.json",
        help="Path to static configuration"
        )
        
        with open(Path(parser.parse_args().config), "r") as jsonfile:
            config = json.load(jsonfile)

        # Creation of Manager proxy and Manager Lock: Manager Server Process with common data for multiprocessing. Not shared memory
        system_status_proxy = manager.dict(Status()._asdict()) # create a proxy dict
        system_status_lock = manager.Lock()
        # shared memory queue
        q_telegram_log = Queue(maxsize=20)

        q_telegram_log.put("Starting Draco")

        # Creation of processes
        processes = []
        # Telegram bot
        processes.append(TelegramBot(config=config, 
                                     memory_proxy=(system_status_proxy, system_status_lock), 
                                     telegram_queue=q_telegram_log,
                                     name="telegram_bot"))
        # Relay shield
        processes.append(GPIOHandler(config=config, 
                                         memory_proxy=(system_status_proxy, system_status_lock), 
                                         telegram_queue=q_telegram_log,
                                         name="relayshield"))
        #System Scheduler
        processes.append(SystemScheduler(config=config, 
                                         memory_proxy=(system_status_proxy, system_status_lock), 
                                         telegram_queue=q_telegram_log,
                                         name="scheduler"))

        # Start processes
        for process in processes:
            process.start()
        
        # main loop for monitoring processes
        while success:
            for process in processes:
                if process.exitcode == 1:
                    raise Exception("A critical process exited with error, terminating all other processes")
            sleep(1)
        
    except Exception as error:
        print(f"Process {pid} - " + repr(error))
        success = False
    finally:
        GPIO.cleanup()
        q_telegram_log.close()
        if processes is not None:
            [p.kill() for p in processes if p.is_alive()]
    return int(not success)

if __name__ == "__main__":
    manager = Manager()
    exit_code = main(manager)
    sys.exit(exit_code)