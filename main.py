import LCD_1in44
import LCD_Config

import RPi.GPIO as GPIO

import Image
import ImageDraw
import ImageFont
import ImageColor
import time
import traceback

LEFT    =   5  # Joypad left
RIGHT   =  26  # Joypad right
UP      =   6  # Joypad up
DOWN    =  19  # Joypad down
LEFTCTRL=  21  # 'A' button
LEFTALT =  20  # 'B' button
SPACE   =  13  # 'Select' button
ENTER   =  16  # 'Start' button

def my_callback(channel):
        print 'PUSHED!'

def main():
	LCD = LCD_1in44.LCD()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ENTER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(SPACE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(SPACE, GPIO.RISING)
        GPIO.add_event_callback(SPACE, my_callback)

        while GPIO.input(ENTER) == GPIO.HIGH:
            time.sleep(0.01)  # wait 10 ms to give CPU chance to do other things

	print "**********Init LCD**********"
	Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
	LCD.LCD_Init(Lcd_ScanDir)
	
	image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
	draw = ImageDraw.Draw(image)
	#font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
	print "***draw line"
	draw.line([(0,0),(127,0)], fill = "BLUE",width = 5)
	draw.line([(127,0),(127,127)], fill = "BLUE",width = 5)
	draw.line([(127,127),(0,127)], fill = "BLUE",width = 5)
	draw.line([(0,127),(0,0)], fill = "BLUE",width = 5)

        name = raw_input("Enter your name: ")

	print "***draw rectangle"
	draw.rectangle([(18,10),(110,20)],fill = "RED")
	print "***draw text"
	draw.text((33, 22), name, fill = "BLUE")

#	draw.text((32, 36), 'Electronic ', fill = "BLUE")
	LCD.LCD_ShowImage(image,0,0)
        name = raw_input("Enter your name: ")
	LCD_Config.Driver_Delay_ms(500)
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

