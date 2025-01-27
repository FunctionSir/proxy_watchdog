# proxy_watchdog
Watch a proxy, and do something if needed.

## How to config
Edit the script directly. Help info about configs is in the script too.

## Recent update
1. Added "retry" related config.
2. You can control the "heartbeat reports" now.
3. The script is more readable now (maybe...).

## How to update
1. Backup your old config.
2. Replace the old scrip with the new one.
3. Reconfigure.

Update is not necessary, if you think the old one is good enough.

## Another way of update (dirty)
1. Copy the old config section.
2. Replace the old scrip with the new one.
3. Paste the old config section UNDER the config section of the new script.
4. Change some new config entries.

THIS WAY IS NOT RECOMMENDED AT ALL!!!

## How to use
1. First, you need Python 3, not 2.
2. Use "nohup" or run it as a service.

An example of using "nohup":
``` bash
nohup python3 -u proxy_watchdog.py > proxy_watchdog.out &
```
