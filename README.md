Cowin bot

after cloning the repo make sure you install pyyaml and playsound dependencies first(in cmd: pip install pyyaml playsound). Add your pincode(s) (if more than one pincode,
seperate them by spaces) in the application.yml file under resources/

you can also set other configurations in the application.yml like the bot timeout, (the time in seconds after which
it will check for updates)

finally, run the script (cmd: python cowin.py)
if the slot is found for any of the pincodes, the updates will stop, and a tone will be played :3
