import country_converter as coco
import pandas as pd

from data_constructor import Constructor

cc = coco.CountryConverter()


def melter(data, id_until, var_name, value_name="value", cut_column=None):
    if cut_column:
        data = data.drop(data.columns[cut_column], axis=1)
    data = data.melt(
        id_vars=data.columns[:id_until],
        value_vars=data.columns[id_until:],
        var_name=var_name,
        value_name=value_name)
    return data



class Importer:
    def __init__(self, filename, mapping_includes_metric=False, mapping=None, metric=None, header_row=None, format="csv"):

        if mapping is None:
            mapping = {"Year": "year", "Code": "country", "Oil": "value"}
        if mapping and mapping_includes_metric:
            pass
        if not mapping_includes_metric:
            self.metric = metric
        if format == "csv":
            if header_row is None:
                self.file = pd.read_csv(filename)
            else: self.file = pd.read_csv(filename, header=header_row)
        if format == "excel" or format == "xlsx" or format == "xls":
            if header_row is None:
                self.file = pd.read_excel(filename)
            else: self.file = pd.read_excel(filename, header=header_row)
        else: print("Format not supported")

        self.keys = mapping

    def melt(self, id_until, var_name, value_name="value", cut_column=None):
        self.file = melter(self.file, id_until, var_name, value_name, cut_column)
        self.file.to_csv("test.csv", index=False)
        # TODO PROPERLY SEPERATE OUT self.file and the data that actually gets modified
        # TODO RETHINK CLASS INITIALISATION AND FUNCTIONS

    def get_data(self):
        # Remove every column but the ones we want THATS SO DUMB
        data = self.file[list(self.keys.values())]
        # Remap
        data = data.rename(columns=self.keys)
        # data = data[list(self.keys.values())]

        # data["metric"] = self.metric # DUMB
        data = data.rename(columns={"value": self.metric})
        data["country"] = cc.pandas_convert(data["country"], to="ISO3")
        data = data[data["country"] != "not found"]

        data["year"] = pd.to_numeric(data["year"], errors="coerce") # TODO FIND A BETTER SOLUTION THAN THIS

        return data
