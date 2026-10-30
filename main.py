import numpy as np
import pandas as pd

import parsers.parser_v2 as parser
import statsmodels.api as sm
from linearmodels.panel import RandomEffects, PanelOLS

# Try to replicate Ross 2001 (ish)
def ross2001():
    df2010 = parser.import_worldbank_oil_rents() # OilRentsGDP
    df2010 = df2010.merge(parser.import_worldbank_mineral_rents()) #MineralRentsGDP
    df2010 = df2010.merge(parser.import_worldbank_income_capita()) #IncomeCapita
    df2010["IncomeCapita"] = np.log(df2010["IncomeCapita"])
    df2010 = df2010.merge(parser.filter_polity(parser.import_polity5())) #polity
    df2010 = df2010[df2010["year"]==2010]
    df2010 = df2010.merge(parser.import_muslim_perc(2010)) #muslim_perc

    oecd = parser.import_OECD(2010)
    df2010["OECD"] = df2010["country"].isin(oecd["country"]).astype(int) #OECD

    df2010reg = df2010.dropna()
    X = sm.add_constant(df2010reg[["OilRentsGDP", "MineralRentsGDP", "IncomeCapita", "muslim_perc", "OECD"]])
    y = df2010reg[["polity"]]

    model = sm.OLS(y, X).fit()
    print(model.summary())

    print(df2010reg[["IncomeCapita", "OECD"]].corr())


    df2010.to_csv("testing.csv")

    # print(parser.import_muslim_perc(2010))


# Try to replicate table 3.8 from Ross 2012
def ross2012():
    df = parser.import_ross_2012()

    # Column 1:
    ## Lagged Polity score, Log Income, Period Dummies
    # Only keep data we want
    df1 = df[["year", "id", "polity", "logGDP_cap2000_sup"]]
    # Create lagged variables
    df1["polity_l5"] = df1.groupby("id")["polity"].shift(5)
    # All the other variables are also lagged by 5 years!
    df1["logGDP_cap2000_sup_l5"] = df1.groupby("id")["logGDP_cap2000_sup"].shift(5)

    # Only keep every 5th year
    # First, change column from datetime to int
    df1_5 = df1[(df["year"]).dt.year % 5 == 0]
    # Create the dummies for each year that is left after only keeping every 5 years
    # If the year is 1960, the column 1960 will be set to 1
    period_dummies = pd.get_dummies(df1_5["year"].dt.year, dtype=int)
    # Join the two tables
    df1_5 = df1_5.join(period_dummies)



    # Define dependent variable names
    # Use all periods BUT one which is the baseline
    # periods = [1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005]
    periods = [1960, 1965, 1970, 1975, 1980, 1985, 1995, 2000, 2005] # 1990 Baseline
    xs = ["polity_l5", "logGDP_cap2000_sup_l5"] + periods # xs = regressor names

    # Get the final dataframe for regression
    d = df1_5[["id", "year", "polity"] + xs]
    # print(d.size)
    d = d.dropna() # Remove missing values
    # print(d.size)

    # Remove all columns where there is only one value (usually 0)
    xs = [x for x in xs if d[x].nunique() > 1]
    d = d[["id", "year", "polity"] + xs]

    # This is needed for the linear model
    # Result: id = AFG year=1970,1975,...    id = AGO year=year=1970,1975,...
    d = d.set_index(["id", "year"])

    # Independent variable
    y = d["polity"]
    # Dependent variable
    X = d.drop(columns="polity")
    # Add a constant
    X = sm.add_constant(X)

    # Set up the regression
    # Because countries are correlated within themselves, we need to tell it to calculate a standard error that is clustered
    res = RandomEffects(y, X).fit(cov_type="clustered", cluster_entity=True)

    # print(d)
    print(res.summary)
    #print(res.params[["const", "polity_l5", "logGDP_cap2000_sup_l5"]])
    #print(res.std_errors[["const", "polity_l5", "logGDP_cap2000_sup_l5"]])
    #print(res.pvalues)
    print(res.nobs, res.entity_info["total"]) # = 1032 170.0



# Replicate Ross 2012 with less messy data

def ross2012_better():
    ross12 = parser.import_ross_2012()


ross2012()