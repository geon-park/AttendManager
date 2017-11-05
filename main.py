from manager.etorrentmanager import ETorrentManager
from manager.twocpumanager import TwoCPUManager
from manager.torenzoamanager import TorenzoaManager
import json
import logging
import logging.handlers
import sys


def str_to_class(name):
    return getattr(sys.modules[__name__], name)


if __name__ == "__main__":
    with open('settings.json', encoding='utf-8') as file:
        # set logger
        logger = logging.getLogger('attendLogger')

        formatter = logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)s][%(levelname)s] %(message)s')

        fileHandler = logging.handlers.RotatingFileHandler('./result.log', maxBytes=5*1024*1024, backupCount=1)
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)
        logger.addHandler(streamHandler)

        logger.setLevel(logging.DEBUG)

        # attend manager
        json_data = json.load(file)
        for name, config in json_data.items():
            if config['enable']:
                encoding = config['encoding']
                del(config['enable'])
                del(config['encoding'])
                handler = str_to_class(name + 'Manager')(**config)
                if handler.attend_today(encoding=encoding):
                    log = name + ' Login succeeded!!'
                    logger.info(log)
                else:
                    log = name + '  Login failed!!'
                    logger.error(log)
