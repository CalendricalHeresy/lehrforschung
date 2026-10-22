from unittest import case

import pandas as pd
import country_converter as coco

def map_columns(mapping, discard_leftovers=False):
    # First deal with duplicate names



    pass

def clean_up(data, column_names=None, columns=None, axis=1):
    """
    cleans up columns either by name or by index
    :param data: Dataframe to be cleaned
    :param column_names: The names of the columns to be removed
    :param columns: The indexes of the columns to be removed
    :param axis: 0 means removing by row labels and 1 means removing columns
    :return:
    """
    if column_names:
        return data.drop(column_names, axis=axis)
    if columns:
        return data.drop(data.columns(columns), axis=axis)
    return data

def easy_melter(data, id_until, var_name, value_name="value"):
    """
    Melts (unpivots) data in the selected range
    :param data: Dataframe that needs to be melted
    :param id_until: The last column BEFORE the data
    :param var_name: the name of the column that has all the values from the column names (x-axis): 1970 | 1971 | 1972
    :param value_name: the name of the column that has the values of the rows (y-axis)
    :param cut_column:
    :return:
    """

    data = data.melt(
        id_vars=data.columns[:id_until],
        value_vars=data.columns[id_until:],
        var_name=var_name,
        value_name=value_name)
    return data

def import_file(file, file_format="csv", header_row=0):
    match file_format:
        case "csv":
            return pd.read_csv(file, header=header_row)
        case "excel" | "xlsx" | "xls":
            return pd.read_excel(file, header=header_row)
        case _:
            raise Exception(f"Invalid file format: {file_format}")


def country_convert(data, column_name, drop_invalid=False):
    """
    Converts any country codes / names to ISO3
    :param data:
    :param column_name:
    :param drop_invalid:
    :return:
    """
    cc = coco.CountryConverter()
    data[column_name] = cc.pandas_convert(data[column_name], to="ISO3")
    if drop_invalid:
        data = data[
            # Conditions for keeping the row
            data["country"] != "not found"
        ]
    return data


def year_convert(data, column_name):
    """
    Converts the year column to an integer
    :param data:
    :param column_name:
    :return:
    """
    data[column_name] = pd.to_numeric(data[column_name], errors="coerce")
    return data



