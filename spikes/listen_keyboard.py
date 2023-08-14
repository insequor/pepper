# Standard Improts
import logging

# Third Party Imports
import keyboard 

# Internal Imports 

TRIGGER_HOTKEY = "capslock"
# NOTE: We should not need quit hotkey, we will use the app icon tro handle this
# or have an exit command in the application
QUIT_HOTKEY = "ctrl+q"


class App:
    stop = False
    active = False

def onQuit():
    logging.debug("quit")
    App.stop = True 


def onTriggerPress():
    if App.active:
        return 
    App.active = True
    logging.debug(f"{TRIGGER_HOTKEY} was pressed!")


def onTriggerRelease():
    if not App.active:
        return 
    App.active = False
    logging.debug(f"{TRIGGER_HOTKEY} was released!")


def main():
    logging.info("Start Listening Keyboard")
    
    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerPress, suppress=True, trigger_on_release=False)
    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerRelease, suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(QUIT_HOTKEY, onQuit, suppress=True)
    
    # Enter to the listening loop
    # keyboard.wait()
    
    # Alternatively we can manage the event loop ourselves
    while not App.stop:
        # Wait for the next event.
        event = keyboard.read_event()
        # if event.event_type == keyboard.KEY_DOWN and event.name == 'space':
        #    print('space was pressed')


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
