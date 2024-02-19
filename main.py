from bot import DexterBot
import threading
import logging
import os

BOLD_LAVENDER = "\033[1m\033[38;5;183m"
RESET = "\033[0m"
logging.basicConfig(level=logging.INFO,
                    format=BOLD_LAVENDER + "%(asctime)s %(name)s.%(levelname)s: %(message)s" + RESET,
                    datefmt='%Y-%m-%d %H:%M:%S')

def run_bot(user, password, host):
    with DexterBot(user, password, host, login_type='berkeley') as dexterbot:
        dexterbot.run()

def main():
    user = os.getenv('CALCENTRAL_USERNAME')
    password = os.getenv('CALCENTRAL_PASSWORD')
    hostnames_str = os.getenv('POLLEV_HOSTNAMES')

    hosts = [host.strip() for host in hostnames_str.split(',')]

    bots =[{'user': user, 'password': password, 'host': host} for host in hosts]

    threads = []
    for bot in bots:    
        t = threading.Thread(target=run_bot, kwargs=bot)
        t.start() 
        threads.append(t)
    
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
