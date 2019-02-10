import os

from action import Action


class MainMenuMachine(object):
    def __init__(self, screen):
        self.state = ShowDevicesSelectedMenuState(screen)
        self.screen = screen

    def on_event(self, event):
        self.state = self.state.on_event(event)

    def select_callback(self, callback):
        self.on_event(Action.SELECT)

    def up_callback(self, callback):
        self.on_event(Action.UP)

    def down_callback(self, calback):
        self.on_event(Action.DOWN)

    def left_callback(self, calback):
        self.on_event(Action.LEFT)

    def right_callback(self, calback):
        self.on_event(Action.RIGHT)


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


class UpdateState(MenuState):
    def draw(self):
        os.system("git pull > /tmp/update_status")
        update_status = open('/tmp/update_status', 'r').read()
        self.screen.draw('update:\n' + update_status)

    def on_event(self, event):
        if event == Action.LEFT:
            return UpdateSelectedMenuState(self.screen)
        return self


class UpdateSelectedMenuState(MenuState):
    def draw(self):
        self.screen.draw_main_menu(self)

    def on_event(self, event):
        if event == Action.UP:
            return MakeBackupSelectedMenuState(self.screen)
        elif event == Action.DOWN:
            return RebootSelectedMenuState(self.screen)
        elif event == Action.SELECT:
            return UpdateState(self.screen)
        return self


class RebootState(MenuState):
    def draw(self):
        self.screen.draw('reboot...')
        os.system('reboot')


class RebootSelectedMenuState(MenuState):
    def draw(self):
        self.screen.draw_main_menu(self)

    def on_event(self, event):
        if event == Action.UP:
            return UpdateSelectedMenuState(self.screen)
        elif event == Action.DOWN:
            return ShutdownSelectedMenuState(self.screen)
        elif event == Action.SELECT:
            return RebootState(self.screen)
        return self


class ShutdownState(MenuState):
    def draw(self):
        self.screen.draw('power off...')
        os.system('poweroff')


class ShutdownSelectedMenuState(MenuState):
    def draw(self):
        self.screen.draw_main_menu(self)

    def on_event(self, event):
        if event == Action.UP:
            return RebootSelectedMenuState(self.screen)
        elif event == Action.SELECT:
            return ShutdownState(self.screen)
        return self


class MakeBackupSelectedMenuState(MenuState):
    def draw(self):
        self.screen.draw_main_menu(self)

    def on_event(self, event):
        if event == Action.UP:
            return ShowDevicesSelectedMenuState(self.screen)
        if event == Action.DOWN:
            return ShutdownSelectedMenuState(self.screen)
        return self


class ShowDevicesState(MenuState):
    def draw(self):
        os.system("df -h | grep media | awk '{print $5 \" \" $6}' > /tmp/media_list")
        media_list = open('/tmp/media_list', 'r').read()
        self.screen.draw('usage device\n' + media_list)

    def on_event(self, event):
        if event == Action.LEFT:
            return ShowDevicesSelectedMenuState(self.screen)
        return self


class ShowDevicesSelectedMenuState(MenuState):
    def draw(self):
        self.screen.draw_main_menu(self)

    def on_event(self, event):
        if event == Action.DOWN:
            return MakeBackupSelectedMenuState(self.screen)
        elif event == Action.SELECT:
            return ShowDevicesState(self.screen)
        return self
