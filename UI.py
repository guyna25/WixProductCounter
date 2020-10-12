import PySimpleGUI as sg

BROWSE_KBD = 'Browse'


class GUI_handler():
    """
    This class handles the Gui of this software
    """

    def __init__(self):
        sg.theme('Dark Blue 3')
        self.window = None

    def browse_csv_window(self, csv_type):
        """
        This method asks the user to choose a csv or excel file
        :return: The path to the chosen file, otherwise, None.
        """
        layout = [[sg.Text('Please choose a ' + csv_type)],
                  [sg.Input(), sg.FileBrowse()],
                  [sg.OK(), sg.Cancel()]]

        window = sg.Window('BickBeautifier', layout)
        event, values = window.read()
        window.close()
        return values.get(BROWSE_KBD)

    def list_handler(self, products):
        """Creates a list with matching products from saved file
           @:return A list with all products
        """
        pass

    def interactive_table(self, items, column_names, preset_values=None, value_size=(40, 1),
                          column_background_color="blue",
                          background_color="blue",
                          text_color="white"):
        # for some unknown reason the size of the first box has 5 pixels more by default
        head = [sg.Text(column_names[0], size=(value_size[0] - 5, value_size[1]),
                        background_color=column_background_color)] + \
               [
                   sg.Text(column_names[i], size=value_size,
                           background_color=column_background_color)
                   for i
                   in range(1, len(column_names))
               ]
        rows = []
        for item in items:
            rows += [
                sg.InputText(default_text=value, size=value_size, background_color=background_color)
                for value
                in item
            ]
        layout = [head, rows, [sg.OK()]]
        # Create the Window
        window = sg.Window('Window Title', layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
                break
            print('You entered ', values[0])

    def close_win(self):
        if (self.window):
            self.window.close()

    def get_product_order(self):
        pass

    def finish_run(self, msg):
        layout = [[sg.Text(msg)], [sg.OK()]]
        window = sg.Window('Bick beautifier', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'OK':  # if user closes window or clicks cancel
                break
