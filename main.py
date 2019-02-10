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
    def __init__(self, screen):
        self.screen = screen
        print 'Processing current state:', str(self)
        self.draw()

    def draw(self):
        pass

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass

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
    def draw(self):
        self.screen.draw_main_menu(self)
        
    def on_event(self, event):
        if event == 'down':
            return MakeBackupSelectedMenuState(self.screen)
        elif event == 'select':
            return ShowDevicesState(self.screen)
        return self


class ShowDevicesState(MenuState):
    def draw(self):
        os.system("df -h | grep media | awk '{print $5 \" \" $6}' > /tmp/media_list")
        media_list = open('/tmp/media_list', 'r').read()
        self.screen.draw('usage device\n' + media_list)
        
    def on_event(self, event):
        if event == 'left':
            return ShowDevicesSelectedMenuState(self.screen)
        return self


class MakeBackupSelectedMenuState(MenuState):
    def draw(self):
        self.screen.draw_main_menu(self)
        
    def on_event(self, event):
        if event == 'up':
            return ShowDevicesSelectedMenuState(self.screen)
        if event == 'down':
            return ShutdownSelectedMenuState(self.screen)
        return self


class ShutdownSelectedMenuState(MenuState):
    def draw(self):
        self.screen.draw_main_menu(self)
        
    def on_event(self, event):
        if event == 'up':
            return MakeBackupSelectedMenuState(self.screen)
        elif event == 'select':
            os.system('poweroff')
        return self


class MainMenuMachine(object):
    def __init__(self, screen):
        self.state = ShowDevicesSelectedMenuState(screen)
        self.screen = screen

    def on_event(self, event):
        self.state = self.state.on_event(event)

    def select_callback(self, callback):
        self.on_event('select')

    def up_callback(self, callback):
        self.on_event('up')

    def down_callback(self, calback):
        self.on_event('down')

    def left_callback(self, calback):
        self.on_event('left')

    def right_callback(self, calback):
        self.on_event('right')


class ScreenController(object):
    def __init__(self, LCD):
        self.LCD = LCD

    def draw_main_menu(self, state):
        draw, image = draw_base_screen(self.LCD)
        print "***draw main menu"
        draw.text((10, 22), ('[X]' if isinstance(state, ShowDevicesSelectedMenuState) else '[ ]') + ' Show devices', fill="BLUE")
        draw.text((10, 36), ('[X]' if isinstance(state, MakeBackupSelectedMenuState) else '[ ]') + ' Copy', fill="BLUE")
        draw.text((10, 50), ('[X]' if isinstance(state, ShutdownSelectedMenuState) else '[ ]') + ' Shutdown', fill="BLUE")
        self.LCD.LCD_ShowImage(image, 0, 0)
    
    def draw(self, text): 
        draw, image = draw_base_screen(self.LCD)
        print "***draw main menu"
        draw.text((10, 22), text, fill="BLUE")
        self.LCD.LCD_ShowImage(image, 0, 0)


def main():
    LCD = LCD_1in44.LCD()
    screen = ScreenController(LCD)

    print "**********Init LCD**********"
    Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    LCD.LCD_Init(Lcd_ScanDir)

    draw_splash_screen(LCD)
    LCD_Config.Driver_Delay_ms(500)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(KEY_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(KEY_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(SELECT, GPIO.RISING)
    GPIO.add_event_detect(UP, GPIO.RISING)
    GPIO.add_event_detect(DOWN, GPIO.RISING)
    GPIO.add_event_detect(LEFT, GPIO.RISING)
    GPIO.add_event_detect(RIGHT, GPIO.RISING)

    while GPIO.input(KEY_3) == GPIO.HIGH:
        time.sleep(0.01)  # wait 10 ms to give CPU chance to do other things
        
    main_menu_machine = MainMenuMachine(screen)
    GPIO.add_event_callback(SELECT, main_menu_machine.select_callback)
    GPIO.add_event_callback(UP, main_menu_machine.up_callback)
    GPIO.add_event_callback(DOWN, main_menu_machine.down_callback)
    GPIO.add_event_callback(LEFT, main_menu_machine.left_callback)
    GPIO.add_event_callback(RIGHT, main_menu_machine.left_callback)

    while GPIO.input(KEY_1) == GPIO.HIGH:
        time.sleep(0.01)  # wait 10 ms to give CPU chance to do other things

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
