import os

import pandas as pd

ARG_NUM = 1
PAYMENT_METHOD = "אשראי"
MARK_CHAR = "V"
TAX_FACTOR = 1.17
OUTPUT_NAME = "result.csv"
csv_name = ""
DEFAULT_ENCODING = "utf-8"


class csv_arranger():
    """
    This object has methods for the specific transformation of the wix site product output
    """

    def get_column_items(self, data, name):
        """This function produces the product names from the user csv"""
        return data[name].unique()

    def extract_info(self, columns, item_dict, temp_df):
        """
        Extracts relevent info from a df
        :param columns: the column names of the csv
        :param item_dict: dicionary that matches between item name in the csv and in the output table
        :param temp_df: the diff with current matching rows
        :return:
        """
        columns = list(columns)
        res = [0] * len(columns)
        for idx, row in temp_df.iterrows():
            res[0] = row["Date"]
            res[1] = row["Billing Customer"]
            res[2] += row["Qty"]  # products purchased
            try:
                res[columns.index(item_dict[row["Item's Name"]])] += row["Qty"]
            except Exception as e:
                print(item_dict)
            res[-1] = "V"  # invoice receipt
            res[-2] = "אשראי"  # payment method
            res[-3] = "סופק"  # soopak
            res[-4] = row["Total"] / TAX_FACTOR  # income with no tax
            res[-5] = row["Total"]  # income with tax
            res[-6] = row["Shipping"]  # shipping
        return res

    def transform_csv(self, csv_filepath, columns, item_dict, used_args='all', output_name="result"):
        """
        Transform the csv into a user product purchase count by date form
        :param csv_filepath: the path to the csv to transform
        :param columns: the column of the csv
        :param item_dict: dicionary that matches between item name in the csv and in the output table
        :param used_args: the agruments relveant to the csv transform, default is to use all df columns
        :param output_name: the name of the result csv
        :return: The transformed csv
        """
        res = pd.DataFrame(columns=columns)
        row_idx = 0
        df = pd.read_csv(csv_filepath)
        if (not used_args == 'all'):
            df = df[used_args]
        for idx, date_group in df.groupby("Date"):
            for useless_idx, daily_customer_purchase in date_group.groupby("Billing Customer"):
                new_row = self.extract_info(columns, item_dict, daily_customer_purchase)
                res.loc[row_idx] = new_row
                row_idx += 1
            res.to_csv(path_or_buf=os.path.dirname(os.path.realpath(__file__)) + "\\" + OUTPUT_NAME, columns=columns[
                                                                                                             :-1],
                       encoding='ISO-8859-8')

    def get_column_names(self, csv_path, encoding=DEFAULT_ENCODING):
        """
        :param csv_path:The path to the the csv file
        :param encoding: the encoding of the csv (mainly relevant for non-english files)
        :return: the column names in the file, note that this method assumes the columns are named
        """
        return pd.read_csv(csv_path, encoding=encoding).columns
