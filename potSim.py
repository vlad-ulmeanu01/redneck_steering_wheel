import serial
import time
import vgamepad

gamepad = vgamepad.VX360Gamepad()
gamepad.reset()

buttons = [(8, vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A),
           (4, vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B),
           (2, vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X),
           (1, vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y)]

def conv4Buttons3Buttons(x: int) -> int:
    #if I need to function with only 3 buttons instead of 4:
    #pushed brake => upshift becomes downshift.
    
    if (x & 8) != 0 and (x & 2) != 0:
        x ^= 3
    return x

collectPeriod = 0.025 #once every ?? seconds, the controller sends something.

conn = serial.Serial(port = "COM3", baudrate = 9600, timeout = 0.1)

sQueued = "" #multiple strings may arrive at once, need a queue for them.

while True:
    sQueued += conn.readline().decode("utf-8")

    first_split = sQueued.find('\r')
    if first_split == -1:
        first_split = len(sQueued)

    s = sQueued[:first_split].strip()
    sQueued = sQueued[first_split+1:].lstrip()

    pot, buttonMask = map(int, s.split()) if s != "" else (None, None)

    if pot != None and buttonMask != None:
        #[0, 1023] -> [-1, 1].
        xval = (pot / 1023 * 2 - 1)
        xval *= 3
        xval = max(xval, -1.0)
        xval = min(xval,  1.0)
        gamepad.left_joystick_float(x_value_float = xval, y_value_float = 0.0)

        buttonMask = conv4Buttons3Buttons(buttonMask)
        for mask, button in buttons:
            if buttonMask & mask: #should press.
                gamepad.press_button(button)
            else: #should release.
                gamepad.release_button(button)

        gamepad.update()

    time.sleep(0.1 * collectPeriod)
