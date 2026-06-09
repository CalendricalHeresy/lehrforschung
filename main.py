from data_constructor import IndConstructor, MultConstructor
import pandas as pd
from parsers.parser_general import Importer

metric_data = {}
all_data = MultConstructor()


def importer(metric, year, country, value=None):
    pass

def individual_data(metric, year, country, value=None):
    if metric not in metric_data.keys():
        metric_data[metric] = IndConstructor(metric)
        metric_data[metric].add_data(year, country, value)
    pass

def large_csv(metric, year, country, value=None):
    pass


if __name__ == '__main__':

    # all_data.add_data("GDP",2021,"GER", 40)
    # all_data.add_data("Population",2021,"GER", 6)
    # all_data.add_data("Population", 2021, "USA", 9)

    #print(all_data.df)
    #print(all_data.get_value("GDP", 2021, "GER"))
#
    #print(all_data.filter({"year": 2021, "country": "GER"}))

    Imp = Importer("data/owid/oil-prod-per-capita/oil-prod-per-capita.csv", mapping={"Year": "year", "Code": "country", "Oil": "value"}, metric="OilProdPerCapita")
#
    all_data = Imp.import_to(all_data)
    print(all_data.df)

    Imp2 = Importer("data/worldbank/oil-rents-share-of-gdp/API_NY.GDP.PETR.RT.ZS_DS2_en_csv_v2_2051.csv", mapping={"Year": "year", "Country Code": "country", "Oil": "value"}, metric="OilRentsShare", header_row=2)
    Imp2.melt(4, "year", cut_column=-1)
    all_data = Imp2.import_to(all_data)

    # WHY ARE YEARS STRINGS AHHHHH
    #TODO ADD VALUE TYPES TO MAPPING!!!!
    all_data.df["year"] = pd.to_numeric(all_data.df["year"], errors="coerce")
    print(all_data.df)
    # print(all_data.filter({"year": 2018, "country":"DEU"}))
    print(all_data.df[
              (all_data.df["country"] == "DEU") &
              # (all_data.df["metric"] == "OilRentsShare") &
              (all_data.df["year"] == 2016)
          ])

    all_data.df.to_csv("test1.csv")



