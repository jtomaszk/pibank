import time

import RPi.GPIO as GPIO

import LCD_1in44
import LCD_Config
from menu import MainMenuMachine
from screen_controller import ScreenController

LEFT = 5  # Joypad left
RIGHT = 26  # Joypad right
UP = 6  # Joypad up
DOWN = 19  # Joypad down
SELECT = 13  # Joypad select
KEY_1 = 21
KEY_2 = 20
KEY_3 = 16


def main():
    LCD = LCD_1in44.LCD()
    screen = ScreenController(LCD)

    print "**********Init LCD**********"
    Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  # SCAN_DIR_DFT = D2U_L2R
    LCD.LCD_Init(Lcd_ScanDir)

    screen.draw_splash_screen()
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


if __name__ == '__main__':
    main()
