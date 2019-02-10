import os
import time

import Image
import ImageDraw
import RPi.GPIO as GPIO

import LCD_1in44
import LCD_Config

LEFT = 5  # Joypad left
RIGHT = 26  # Joypad right
UP = 6  # Joypad up
DOWN = 19  # Joypad down
SELECT = 13  # Joypad select
KEY_1 = 21
KEY_2 = 20
KEY_3 = 16


class MenuState(object):
    def __init__(self):
        print 'Processing current state:', str(self)

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass

    def label(self):
        return self.__str__()

    def __repr__(self):
        """
        Leverages the __str__ method to describe the State.
        """
        return self.__str__()

    def __str__(self):
        """
        Returns the name of the State.
        """
        return self.__class__.__name__


class ShowDevicesSelectedMenuState(MenuState):
    def on_event(self, event):
        if event == 'down':
            return MakeBackupSelectedMenuState()
        return self


class MakeBackupSelectedMenuState(MenuState):
    def on_event(self, event):
        if event == 'up':
            return ShowDevicesSelectedMenuState()
        if event == 'down':
            return ShutdownSelectedMenuState()
        return self


class ShutdownSelectedMenuState(MenuState):
    def on_event(self, event):
        if event == 'up':
            return MakeBackupSelectedMenuState()
        elif event == 'select':
            os.system('poweroff')
        return self


class MainMenuMachine(object):
    def __init__(self, LCD):
        self.state = ShowDevicesSelectedMenuState()
        self.LCD = LCD

    def on_event(self, event):
        self.state = self.state.on_event(event)
        self.draw_main_menu()

    def select_callback(self):
        self.on_event('select')

    def up_callback(self):
        self.on_event('up')

    def down_callback(self):
        self.on_event('down')

    def draw_main_menu(self):
        draw, image = draw_base_screen(self.LCD)
        print "***draw main menu"
        draw.text((33, 22), ('*' if isinstance(self.state, ShowDevicesSelectedMenuState) else ' ') + ' Show devices', fill="BLUE")
        draw.text((32, 36), ('*' if isinstance(self.state, MakeBackupSelectedMenuState) else ' ') + 'Copy', fill="BLUE")
        draw.text((32, 50), ('*' if isinstance(self.state, ShutdownSelectedMenuState) else ' ') + 'Shutdown', fill="BLUE")
        self.LCD.LCD_ShowImage(image, 0, 0)


def main():
    LCD = LCD_1in44.LCD()

    print "**********Init LCD**********"
    Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    LCD.LCD_Init(Lcd_ScanDir)

    draw_splash_screen(LCD)
    LCD_Config.Driver_Delay_ms(500)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(KEY_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(SELECT, GPIO.RISING)

    while GPIO.input(KEY_3) == GPIO.HIGH:
        time.sleep(0.01)  # wait 10 ms to give CPU chance to do other things
        main_menu_machine = MainMenuMachine()
        GPIO.add_event_callback(SELECT, main_menu_machine.select_callback)
        GPIO.add_event_callback(SELECT, main_menu_machine.up_callback)
        GPIO.add_event_callback(SELECT, main_menu_machine.down_callback)

    # name = raw_input("Enter your name: ")

    # print "***draw rectangle"
    # draw.rectangle([(18, 10), (110, 20)], fill="RED")
    # print "***draw text"
    # draw.text((33, 22), name, fill="BLUE")

    #	draw.text((32, 36), 'Electronic ', fill = "BLUE")
    # LCD.LCD_ShowImage(image, 0, 0)
    # name = raw_input("Enter your name: ")


def draw_splash_screen(LCD):
    draw, image = draw_base_screen(LCD)
    print "***draw text"
    draw.text((33, 22), "PiBank", fill="BLUE")
    draw.text((32, 50), '   press a KEY3', fill="BLUE")
    LCD.LCD_ShowImage(image, 0, 0)


def draw_base_screen(LCD):
    image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
    draw = ImageDraw.Draw(image)
    print "***draw line"
    draw.line([(0, 0), (127, 0)], fill="BLUE", width=5)
    draw.line([(127, 0), (127, 127)], fill="BLUE", width=5)
    draw.line([(127, 127), (0, 127)], fill="BLUE", width=5)
    draw.line([(0, 127), (0, 0)], fill="BLUE", width=5)
    return draw, image


#	image = Image.open('time.bmp')
#	LCD.LCD_ShowImage(image,0,0)

#        try:
#	    while (True):
#                button_state = GPIO.input(LEFT)
#                if button_state == FALSE:
#                    print "button pressed"
#        except:
#	    print("except")
#            traceback.print_exc()
#	    GPIO.cleanup()

if __name__ == '__main__':
    main()
