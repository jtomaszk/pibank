from menu import UpdateSelectedMenuState, RebootSelectedMenuState, ShutdownSelectedMenuState, MakeBackupSelectedMenuState, ShowDevicesSelectedMenuState


class ScreenController(object):
    def __init__(self, LCD):
        self.LCD = LCD

    def draw_splash_screen(self):
        draw, image = self.draw_base_screen()
        print "***draw text"
        draw.text((33, 22), "PiBank", fill="BLUE")
        draw.text((32, 50), '   press a KEY3', fill="BLUE")
        self.LCD.LCD_ShowImage(image, 0, 0)

    def draw_base_screen(self):
        image = Image.new("RGB", (self.LCD.width, self.LCD.height), "WHITE")
        draw = ImageDraw.Draw(image)
        print "***draw line"
        draw.line([(0, 0), (127, 0)], fill="BLUE", width=5)
        draw.line([(127, 0), (127, 127)], fill="BLUE", width=5)
        draw.line([(127, 127), (0, 127)], fill="BLUE", width=5)
        draw.line([(0, 127), (0, 0)], fill="BLUE", width=5)
        return draw, image

    def draw_main_menu(self, state):
        draw, image = self.draw_base_screen()
        print "***draw main menu"
        draw.text((10, 22), ('[X]' if isinstance(state, ShowDevicesSelectedMenuState) else '[ ]') + ' Show devices', fill="BLUE")
        draw.text((10, 36), ('[X]' if isinstance(state, MakeBackupSelectedMenuState) else '[ ]') + ' Copy', fill="BLUE")
        draw.text((10, 50), ('[X]' if isinstance(state, UpdateSelectedMenuState) else '[ ]') + ' Update', fill="BLUE")
        draw.text((10, 50), ('[X]' if isinstance(state, RebootSelectedMenuState) else '[ ]') + ' Reboot', fill="BLUE")
        draw.text((10, 50), ('[X]' if isinstance(state, ShutdownSelectedMenuState) else '[ ]') + ' Shutdown', fill="BLUE")
        self.LCD.LCD_ShowImage(image, 0, 0)

    def draw(self, text):
        draw, image = self.draw_base_screen()
        print "***draw main menu"
        draw.text((10, 22), text, fill="BLUE")
        self.LCD.LCD_ShowImage(image, 0, 0)