import PySimpleGUI as sg


class MTWindow(sg.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs["title"]
        self.layout = kwargs["layout"]
        self.move_center()

    def move_center(self):

        screen_width, screen_height = self.get_screen_dimensions()
        win_width, win_height = self.size
        x, y = (screen_width - win_width) // 2, (screen_height - win_height) // 2
        self.move(x, y)
