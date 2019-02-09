import traceback

import Image
import ImageColor
import ImageDraw
import ImageFont
import RPi.GPIO as GPIO
import time

import LCD_1in44
import LCD_Config

LEFT = 5  # Joypad left
RIGHT = 26  # Joypad right
UP = 6  # Joypad up
DOWN = 19  # Joypad down
SELECT = 13 # Joypad select
KEY_1 = 21
KEY_2 = 20
KEY_3 = 16


def my_callback(channel):
    print 'PUSHED!'


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
    GPIO.add_event_callback(SELECT, my_callback)

    while GPIO.input(KEY_3) == GPIO.HIGH:
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
    draw.text((32, 50), '     press a KEY3', fill = "BLUE")
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
