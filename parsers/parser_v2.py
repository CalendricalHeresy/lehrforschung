import pandas as pd
import parsers.parser_v2_helpers as hp
import country_converter as coco




def import_worldbank(filename, value_name, header_row=2, remove_last_col=False):
    df = hp.import_file(
        filename,
        file_format="csv",
        header_row=header_row
    )
    if remove_last_col:
        df = hp.clean_up(df, columns=[-1])  # Last column is None throughout so delete it
    df = hp.easy_melter(df, 4, "year")  # Unpivot
    df = hp.map_columns(df, {"Country Code": "country", "year": "year", "value": value_name}, discard_leftovers=True)
    df = hp.year_convert(df, "year")
    df = hp.country_convert(df, "country", drop_invalid=True)
    # print(df[df["year"] == 2010])
    return df

def import_worldbank_oil_rents():
    df = import_worldbank("data/worldbank/oil-rents-share-of-gdp/API_NY.GDP.PETR.RT.ZS_DS2_en_csv_v2_2051.csv",
                     "OilRentsGDP",
                          remove_last_col=True)
    return df

def import_worldbank_mineral_rents():
    df = import_worldbank("data/worldbank/mineral-rents-share-of-gdp/API_NY.GDP.MINR.RT.ZS_DS2_en_csv_v2_10202.csv",
                          "MineralRentsGDP",
                          remove_last_col=True)
    return df

def import_worldbank_income_capita():
    df = import_worldbank("data/worldbank/adjusted-net-national-income-per-capita/API_NY.ADJ.NNTY.PC.CD_DS2_en_csv_v2_38701.csv",
                          "IncomeCapita",
                          remove_last_col=True)
    return df

def import_owid_oil_prod():
    df = hp.import_file(
        "data/owid/oil-prod-per-capita/oil-prod-per-capita.csv",
        file_format="csv",
    )
    df = hp.map_columns(df, {"Year": "year", "Code": "country", "Oil": "OilProdCapita"}, discard_leftovers=True)
    df = hp.year_convert(df, "year")
    df = hp.country_convert(df, "country", drop_invalid=True)
    return df

def import_polity5(data="polity"):
    """

    :param data: Either "polity" or "polity2" or "democ" or "autoc" are useful
    :return:
    """
    # Hackett, Conrad, Marcin Stonawski, Yunping Tong, Stephanie Kramer and Anne Fengyan Shi. 2025. “Dataset of Global Religious Composition Estimates for 2010 and 2020.” Pew Research Center. doi: 10.58094/vhrw-k516.
    df = hp.import_file(
        "data/polity5/p5v2018.xls",
        file_format="xls",
    )
    df = hp.map_columns(df, {"year":"year", "scode":"country", data:data}, discard_leftovers=True)
    pd.to_numeric(df[data], errors="coerce")

    df = hp.year_convert(df, "year")
    df = hp.country_convert(df, "country", drop_invalid=True)
    return df

def filter_polity(df):
    # some values are -66 -77 -88 etc for unclear data
    df = df[df["polity"]>=-10]
    df["polity"] = (df["polity"] + 10)/2
    return df

def import_muslim_perc(year=2010):
    df = hp.import_file(
        "data/pew_research/Religious-Composition-2010-2020-dataset/Religious Composition 2010-2020 dataset/Religious Composition 2010-2020 (percentages).csv",
        file_format="csv",
    )
    df = hp.year_convert(df, "Year")
    df = df[df["Year"]==year]
    df = hp.map_columns(df, {"Year":"year", "Countrycode":"country", "Muslims":"muslim_perc"}, discard_leftovers=True)
    df = hp.country_convert(df, "country", drop_invalid=True)

    return df

def import_OECD(year=2010):
    cc = coco.CountryConverter()
    df = cc.OECDas("ISO3")[cc.OECD["OECD"]<=2010]
    df = df.rename(columns={"ISO3":"country"})
    df["year"] = year
    return df

def import_ross_2012():
    df = hp.import_file(
        "data/ross_data/replicationdataross2012/Replication data for The Oil Curse - Ross 2012.dta",
        file_format="dta"
    )
    return df

def import_ross_2015():
    pass

def import_wb_p_data():
    df = hp.import_file(
        "data/worldbank/P_Data_Extract_From_World_Development_Indicators/data.csv",
        file_format="csv"
    )

    return df

# REMEMBER THAT COUNTRYCONVERTER HAS DATA AS WELL (SUCH AS OECD MEMBERS)



