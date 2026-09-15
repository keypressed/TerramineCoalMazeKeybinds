import pyautogui
from pynput import keyboard
import Quartz

print("[Terramine Coal Maze Keybinds]")
print("> press 'h' to see a list of commands")

# find the iPhone mirroring window and return some attributes about it, mainly the x and y positions
def get_iphone_mirroring_window():
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionOnScreenOnly,
        Quartz.kCGNullWindowID
    )

    for window in windows:
        owner = window.get('kCGWindowOwnerName', '')
        title = window.get('kCGWindowName', '')

        if 'iPhone Mirroring' in owner or 'iPhone Mirroring' in title:
            bounds = window.get('kCGWindowBounds', {})
            return {
                'x': int(bounds.get('X', 0)),
                'y': int(bounds.get('Y', 0)),
                'width': int(bounds.get('Width', 0)),
                'height': int(bounds.get('Height', 0)),
                'title': title,
                'owner': owner
            }
    return None

def darwin_intercept(event_type, event):
    keycode = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
    if keycode in (123, 124, 125, 126):
        return None
    return event

# send a pyautogui click to the coordinates of the respective input arrow
def press_key(direction):
    match direction:
        case "south":
            pyautogui.click((window['x'] + south_offset[0]), (window['y'] + south_offset[1]))
        case "west":
            pyautogui.click((window['x'] + west_offset[0]), (window['y'] + west_offset[1]))
        case "north":
            pyautogui.click((window['x'] + north_offset[0]), (window['y'] + north_offset[1]))
        case "east":
            pyautogui.click((window['x'] + east_offset[0]), (window['y'] + east_offset[1]))
        case _:
            print("could not find direction")

window = get_iphone_mirroring_window()
keybinds = False
south_offset = [110, 665]
west_offset  = [62, 606 ]
north_offset = [114, 554]
east_offset  = [166, 609]

# handles the various character inputs
def on_press(key):
    global keybinds, window
    try:
        error_msg = "keybinds are disabled - press 'h' for more info"
        match key.char:
            case 'a':
                if keybinds:
                    press_key("west")
                else:
                    print(error_msg)
            case 'd':
                if keybinds:
                    press_key("east")
                else:
                    print(error_msg)
            case 'h':
                print("[----Commands----]")
                print("1. 'h' - prints this help menu")
                print("2. 'q' - quits the program")
                print("3. '[' - toggles the keybinds on")
                print("4. ']' - toggles the keybinds off")
                print("5. 'l' - lists available keybinds")
                print("6. 'r' - refreshes keybind locations (use this if you move the phone mirror)")
            case 'l':
                print("Available keybinds: ")
                print("arrow_down, arrow_left, arrow_up, arrow_right")
            case 'q':
                print("Quitting program")
                return False
            case 'r':
                window = get_iphone_mirroring_window()
                print("refreshed keybind coordinates")
            case 's':
                if keybinds:
                    press_key("south")
                else:
                    print(error_msg)
            case 'w':
                if keybinds:
                    press_key("north")
                else:
                    print(error_msg)
            case '[':
                keybinds = True
            case ']':
                keybinds = False
    except AttributeError:
        error_msg = "keybinds are disabled - press 'h' for more info"
        match key:
            case keyboard.Key.down:
                if keybinds:
                    press_key("south")
                else:
                    print(error_msg)
            case keyboard.Key.left:
                if keybinds:
                    press_key("west")
                else:
                    print(error_msg)
            case keyboard.Key.up:
                if keybinds:
                    press_key("north")
                else:
                    print(error_msg)
            case keyboard.Key.right:
                if keybinds:
                    press_key("east")
                else:
                    print(error_msg)

listener = keyboard.Listener(on_press=on_press, darwin_intercept=darwin_intercept)
listener.start()
listener.join()