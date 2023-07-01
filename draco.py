import sys, os
from pathlib import Path
from multiprocessing import Manager
from draco.processors.telegram_bot import TelegramBot
from draco.processors.HW_handler import HardwareHandler
from draco.utils.types import Status
import argparse
import json
import RPi.GPIO as GPIO
from time import sleep


def main(manager) -> int:
    success = True
    processes = None
    pid = os.getpid()
    GPIO.cleanup() #cleanup will be made in main application only
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

        #Creation of Manager proxy and Manager Lock
        system_status_proxy = manager.dict(Status()._asdict()) # create a proxy dict
        system_status_lock = manager.Lock()

        # Creation of processes
        processes = []
        # Telegram bot
        processes.append(TelegramBot(config=config, 
                                     memory_proxy=(system_status_proxy, system_status_lock), 
                                     name="telegram_bot"))
        # Relay shield
        processes.append(HardwareHandler(config=config, 
                                         memory_proxy=(system_status_proxy, system_status_lock), 
                                         name="relayshield"))

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
        print("GPIO cleanup performed due to exitting app")
        if processes is not None:
            for process in processes:
                [p.kill() for p in processes if p.is_alive()]
    return int(not success)

if __name__ == "__main__":
    manager = Manager()
    exit_code = main(manager)
    sys.exit(exit_code)