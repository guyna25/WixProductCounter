import os
import pickle
from time import sleep

import PySimpleGUI as sg
import pandas as pd

import UI
import csvArranger

NEEDED_ARGS = ["Order #", "Date", "Billing Customer", "Item's Name", "Qty", "Shipping", "Total"]
WANTED_COLUMN = "Item's Name"
ROW_WIDTH = 40
ROW_HEIGHT = 1
COLUMN_BACKGROUND_COLOR = "black"
VALUE_BACKGROUND_COLOR = "white"
ENCODING = 'ISO-8859-8'
ITEM_COLUMN_NAME_DICT_PATH = ""
ITEM__NAME_DICT_NAME = "item_name_map"
OUTPUT_NAME = "result.csv"
END_MSG = "Program finished running, you can find the result in %s" % OUTPUT_NAME


def load_column_item_dict(path):
    """
    Loads the dictionary that maps item's full name to the matching column name
    :param path:path to dictionary pkl file
    :return:A dictionary containing mapping of full names to column name
    """
    if (os.path.isfile(path)):
        return pickle.load(path)
    return None  # todo later deal with cases of none existing format


def table_example():
    """
    Table creation example taken from pysimplegui
    """
    sg.set_options(auto_size_buttons=True)
    filename = sg.popup_get_file(
        'filename to open', no_window=True, file_types=(("CSV Files", "*.csv"),))
    # --- populate table with file contents --- #
    if filename == '':
        return

    data = []
    header_list = []
    button = sg.popup_yes_no('Does this file have column names already?')

    if filename is not None:
        try:
            # Header=None means you directly pass the columns names to the dataframe
            df = pd.read_csv(filename, sep=',', engine='python', header=None)
            data = df.values.tolist()  # read everything else into a list of rows
            if button == 'Yes':  # Press if you named your columns in the csv
                # Uses the first row (which should be column names) as columns names
                header_list = df.iloc[0].tolist()
                # Drops the first row in the table (otherwise the header names and the first row will be the same)
                data = df[1:].values.tolist()
            elif button == 'No':  # Press if you didn't name the columns in the csv
                # Creates columns names for each column ('column0', 'column1', etc)
                header_list = ['column' + str(x) for x in range(len(data[0]))]
        except:
            sg.popup_error('Error reading file')
            return

    layout = [
        [sg.Table(values=data,
                  headings=header_list,
                  display_row_numbers=True,
                  auto_size_columns=False,
                  num_rows=min(25, len(data)))]
    ]

    window = sg.Window('Table', layout, grab_anywhere=False)
    event, values = window.read()
    window.close()


def save_obj(obj, name):
    """
    Saves object in binary pickle format
    :param obj: the object to pickle
    :param name: the name under which to save the file
    """
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """
    Loads obj from puckle file
    :param name: name of the file to load
    :return: the object loaded from the pickle file
    """
    if (os.path.isfile('obj/' + name + '.pkl')):
        with open('obj/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)
    return {}


if __name__ == "__main__":

    try:
        # init
        item_name_map = load_obj(ITEM__NAME_DICT_NAME)
        ui = UI.GUI_handler()
        csv_arranger = csvArranger.csv_arranger()
        # file_abs_path = 'C:/Users/guyn2/Desktop/bickbeautifier/orders.csv'
        # template_abs_path ='C:\\Users\guyn2\Desktop\\bickbeautifier\\tenmplate.csv'
        # column_names = csv_arranger.get_column_names(template_abs_path, ENCODING)
        # res = csv_arranger.transform_csv(file_abs_path, column_names, item_name_map, used_args=NEEDED_ARGS)
        # get relevant data from user
        file_abs_path = ui.browse_csv_window("csv to transform")
        template_abs_path = ui.browse_csv_window("column template")
        column_names = csv_arranger.get_column_names(template_abs_path, ENCODING)
        res = pd.DataFrame(columns=column_names)
        # transform csv
        csv_arranger.transform_csv(file_abs_path, column_names, item_name_map, output_name=OUTPUT_NAME)
        # inform about finish
        ui.finish_run(END_MSG)
    except Exception as e:
        print(e)
        sleep(10)
