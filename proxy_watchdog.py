#!/usr/bin/env python3

### TIPS HERE ###
# 0. This script is for Linux, *BSD, or other UNIX-like systems only currently.
# 1. socks5h will resolve domains remotely, not locally (that's what socks5 does)
# 2. A small checking_gap is not friendly to the server you used to check the proxy.
# 3. Please check the config before use it. If you have the abilities, check the source code.
### TIPS ENDS ###

### CONFIG HERE ###
target_proxy = 'socks5h://127.0.0.1:9150' # The proxy you want to check. P.S. You might want socks5h rather than socks5.
checking_url = 'http://google.com' # URL for checking the proxy.
curl_max_time = 10 # Arg max-time for curl, seconds.
checking_gap = 300 # Gap between 2 checks, seconds.
extra_delay_after_post_fail = 120 # Delay more after post fail action done.
curl_bin = '/usr/bin/curl' # Where cURL binary is. P.S. You might don't need to change it.

# What do you want to do after failed checks / succeed checks.
# Use 'python' to use 'eval' to run python code. Use 'system' to exec a shell command using 'os.system'.
post_fail = ('system','systemctl restart tor')
post_success = ('python','None')
### CONFIG ENDS ###

import logging
import os
import signal
import time

def signal_handler(sig, frame):
    logging.info('Goodbye!')
    exit(0)

def runner(data: tuple[str:str]):
    if data[0] == 'python':
        eval(data[1])
    elif data[0] == 'system':
        os.system(data[1])
    else:
        raise ValueError('Tuple element post_fail[0] or post_success[0] must be one of system or python')

print('ProxyWatchdog [ Version: 0.1.0 (ShiraiKuroko) ]')
print('By FunctionSir | Feel free to use it under AGPLv3')

signal.signal(signal.SIGINT, signal_handler)
logging.basicConfig(level=logging.INFO, format='%(asctime)s: [%(levelname)s] %(message)s')

logging.info('Started the watchdog...')
tot_succeed = 0
tot_failed = 0
while True:
    tot_chks = tot_succeed + tot_failed
    if tot_chks > 0 and tot_chks % 1 == 0:
        logging.info('Heartbeat: TotalChecks: '+str(tot_chks)+' Succeed: '+str(tot_succeed)+' Failed: '+str(tot_failed))
    logging.debug('Start to check proxy "'+target_proxy+'"...')
    status = os.system('ALL_PROXY='+target_proxy+' '+curl_bin+' '+checking_url+' --max-time '+str(curl_max_time)+' > /dev/null 2> /dev/null')
    if status == 0:
        tot_succeed += 1
        logging.debug('Test succeed')
        runner(post_success)
    else:
        tot_failed += 1
        logging.warning('Test failed for "'+target_proxy+'" using "'+checking_url+'"')
        runner(post_fail)
        logging.info('Post fail action performed completely. Will sleep for extra '+str(extra_delay_after_post_fail)+'s')
        time.sleep(extra_delay_after_post_fail)
    logging.debug('Done. Will sleep for '+str(checking_gap)+'s')
    time.sleep(checking_gap)
