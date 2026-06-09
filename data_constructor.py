import csv
import pandas as pd


class Constructor:

    def __init__(self, columns):
        self.df = pd.DataFrame(columns=columns)

    def filter(self, columns_dict):
        df_filtered = self.df
        for column, value in columns_dict.items():
            df_filtered = df_filtered[df_filtered[column] == value]
        return df_filtered

    def construct(self, filepath):
        self.df.to_csv(filepath, index=False)


class IndConstructor(Constructor):

    def __init__(self, metric):
        self.metric = metric
        super().__init__(columns=["year", "country", "value"])

    def add_data(self, year, country, value):
        self.df.loc[len(self.df)] = [year, country, value]

    def get_value(self, year, country):
        return self.df.query(f'year == {year} & country == "{country}"')[
            "value"
        ].item()


class MultConstructor(Constructor):

    def __init__(self):
        super().__init__(columns=["metric", "year", "country", "value"])

    def add_data(self, metric, year, country, value):
        self.df.loc[len(self.df)] = [metric, year, country, value]

    def get_value(self, metric, year, country):
        return self.df.query(
            f'metric == "{metric}" & year == {year} & country == "{country}"'
        )["value"].item()





