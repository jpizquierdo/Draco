import sys, os
from pathlib import Path
from multiprocessing import Queue
from draco.processors.telegram_bot import TelegramBot
import argparse
import json
from time import sleep

def main() -> int:
    success = True
    processes = None
    pid = os.getpid()
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
        # Creation of processes
        processes = []
        # Telegram bot
        processes.append(TelegramBot(config=config))

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
        if processes is not None:
            for process in processes:
                [p.kill() for p in processes if p.is_alive()]
    return int(not success)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)