import manager.etorrent
import manager.twocpu
import json
import logging
import logging.handlers

if __name__ == "__main__":
    with open('settings.json') as file:
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
        data = json.load(file)

        enable = data['Login']['ETorrent']['enable']
        username = data['Login']['ETorrent']['username']
        password = data['Login']['ETorrent']['password']
        login_url = data['Login']['ETorrent']['login_url']
        check_url = data['Login']['ETorrent']['check_url']
        attend_url = data['Login']['ETorrent']['attend_url']

        if enable:
            handler = manager.etorrent.ETorrentManager(username=username, password=password, login_url=login_url,
                                                       check_url=check_url, attend_url=attend_url)
            if handler.attend_today(encoding='euc-kr'):
                logger.info('eTorrent Login succeeded!!')
            else:
                logger.error('eTorrent Login failed!!')

        enable = data['Login']['2CPU']['enable']
        username = data['Login']['2CPU']['username']
        password = data['Login']['2CPU']['password']
        login_url = data['Login']['2CPU']['login_url']
        check_url = data['Login']['2CPU']['check_url']
        attend_url = data['Login']['2CPU']['attend_url']

        if enable:
            handler = manager.twocpu.TwoCPUManager(username=username, password=password, login_url=login_url,
                                                   check_url=check_url, attend_url=attend_url)
            if handler.attend_today(encoding='euc-kr'):
                logger.info('2CPU Login succeeded!!')
            else:
                logger.error('2CPU Login failed!!')
